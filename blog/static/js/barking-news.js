function resizeGridItem (item) {
  grid = document.getElementsByClassName("nbt-barking-news-grid")[0];
  rowHeight = parseInt(window.getComputedStyle(grid).getPropertyValue('grid-auto-rows'));
  rowGap = parseInt(window.getComputedStyle(grid).getPropertyValue('grid-row-gap'));
  console.log(rowHeight, rowGap)
  rowSpan = Math.ceil((item.querySelector('.content').getBoundingClientRect().height+rowGap)/(rowHeight+rowGap));
  item.style.gridRowEnd = "span "+ rowSpan;
}

function resizeInstance(instance) {
  item = instance.elements[0];
  resizeGridItem(item);
}

function resizeAllGridItems () {
  allItems = document.getElementsByClassName("item");
  for (i = 0; i < allItems.length; i++) {
    imagesLoaded( allItems[i], resizeInstance);
  }
}

window.onload = resizeAllGridItems();
window.addEventListener("resize", resizeAllGridItems);

// jquery code
$(document).ready(function () {

  $searchBtn = $('[data-action=toggleSearch]')[0];
  $searchForm = $('[data-target=searchForm]')[0];
  $searchIcon = $('[data-target=searchIcon]')[0];
  $searchClose = $('[data-target=searchClose]')[0];
  $searchInput = $('[data-target=searchInput]')[0];

  $($searchBtn).click(function () {
    $($searchForm).toggleClass('hidden');
    $($searchBtn).toggleClass('btn-outline--none').toggleClass('btn-search--close').toggleClass('btn-circle');
    $($searchIcon).toggleClass('hidden');
    $($searchClose).toggleClass('hidden');
    $($searchInput).focus();
  })
})
