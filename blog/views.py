from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from .models import Genre, Post, Comment
from django.db.models import Count

from django.views.generic import ListView
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .forms import EmailPostForm, CommentForm, SearchForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag

class PostListView(ListView):
    queryset = Post.published.all() #we could have specified model = Post and Django would have built the generic Post.objects.all() QuerySet for us.
    context_object_name = 'posts' #default variable is object_list if we don't specify any context_object_name
    paginate_by = 3
    template_name = 'blog/post/list.html' #If we don't set a default template, ListView will use blog/post_list.html.

def barking_news (request, tag_slug=None):
    form = SearchForm()
    object_list = Post.published.all()
    tag = None
    genre_list = Genre.objects.all()

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 6) # 3 posts in each page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    # aside = get_object_or_404(Post, priority='aside')

    return render(request, 'blog/post/list.html', {'page': page,
                                                   'posts': posts,
                                                   'tag': tag,
                                                   'form': form,
                                                   'genres': genre_list})

def about (request):
    genre_list = Genre.objects.all()
    return render(request, 'blog/about.html', {'genres': genre_list})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)

    #List of active comments for a given post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        #A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #Create comment but don't save to DB yet
            new_comment = comment_form.save(commit=False)
            #Assign the current post to the comment
            new_comment.post = post
            #Save the comment to the DB
            new_comment.save()
    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                  .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags','-publish')[:3]

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts,
                  })

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                                          post.get_absolute_url())
            subject = '{} ({}) recommends you read "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'magyarn@umich.edu',
 [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            results = Post.objects.annotate(
                          search=search_vector,
                          rank=SearchRank(search_vector, search_query)
                      ).filter(search=search_query).order_by('-rank')
    return render(request,
                 'blog/post/search.html',
                 {'form': form,
                 'query': query,
                 'results': results})
