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
