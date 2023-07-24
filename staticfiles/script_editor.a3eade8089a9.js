function select_item(editor_number, item_number) {
    /*
    
    editor number is index of editors within a page
    item_number is item index within editor
    id="display_area_0": display area for first editor
    id='item_content_0_3': 3rd item content of editor_0 (hidden by default)
    id="sidebar_item_0_1" // sidebar item of 0th code editor at index 1

    */
      const parentDiv = document.getElementById('display_area_' + editor_number);
      const children = parentDiv.children;
  
      // hide all the children
      for (let i = 0; i < children.length; i++) {
        children[i].style.display = "none";
        // unselect the item
        document.getElementById('sidebar_item_' + editor_number + '_' + i).style.background='transparent';
      }
      
      // Display selected item (code/file)
      document.getElementById('item_content_' + editor_number + '_' + item_number).style.display = "block";

      // Color of selected sidebar item
      document.getElementById('sidebar_item_' + editor_number + '_' + item_number).style.background='black';
  }
  
  // Auto-hide scroll-bar on not selected
  document.addEventListener("DOMContentLoaded", function() {
  const scrollableDiv = document.querySelector(".custom-scrollbar");

  scrollableDiv.addEventListener("scroll", function() {
    if (scrollableDiv.scrollTop === 0) {
      scrollableDiv.classList.remove("scrolling");
    } else {
      scrollableDiv.classList.add("scrolling");
    }
  });
});