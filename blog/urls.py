from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.barking_news, name='barking_news'),
    path('sports/', views.sports, name='sports'),
    path('tag/<slug:tag_slug>/', views.barking_news, name='post_list_by_tag'),
    # path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),
    path('<int:post_id>/share/',
         views.post_share, name='post_share'),
]