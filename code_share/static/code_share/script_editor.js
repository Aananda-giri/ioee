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


// auto-scroll to code part of an editor for smaller screen
document.addEventListener("DOMContentLoaded", function() {
if (window.innerWidth < 768) {
  const displayAreas = document.getElementsByClassName("display-area");

  for (let i = 0; i < displayAreas.length; i++) {

    displayAreas[i].scrollIntoView({ behavior: "auto" });
  }
}
});


function reset_editor(editor_number){
  console.log(`reset_editor(${editor_number})`);
  const code_children = document.getElementById('ul_codes_' + editor_number).children;
  const file_children = document.getElementById('ul_files_' + editor_number).children;

  // hide all the codes
  for (let i = 0; i < code_children.length; i++) {
    
    // unselect all code sidebar items
    console.log('sidebar_code_' + editor_number + '_' + i + ').style.background=transparent');
    document.getElementById('sidebar_code_' + editor_number + '_' + i).style.background='transparent';

    // hide respective code
    console.log('hiding codePreview_' + editor_number + '_' + i);
    document.getElementById('codePreview_' + editor_number + '_' + i).style.display='none';
  }

  // unselect all the files from sidebar
  for (let i = 0; i < file_children.length; i++) {
    console.log('sidebar_file_' + editor_number + '_' + i + ').style.background=transparent');
    document.getElementById('sidebar_file_' + editor_number + '_' + i).style.background='transparent';

    //hide respective file
    console.log('filePreview_' + editor_number + '_' + i + ').style.background=transparent');
    document.getElementById('filePreview_' + editor_number + '_' + i).style.display = "none";
  }

  // hide new file
  document.getElementById('sidebar_file_' + editor_number + '_0').style.display = "none";

  // hide new code
  document.getElementById('sidebar_code_' + editor_number + '_0').style.display = "none";
}

function preview_code(editor_number, item_number) {
  /*
  
  editor number is index of editors within a page
  item_number is item index within editor
  id="display_area_0": display area for first editor
  id='codePreview_0_3': 3rd item content of editor_0 (hidden by default)
  id="sidebar_code_0_1" // sidebar item of 0th code editor at index 1

  */
  console.log(`invoked: preview_file(${editor_number}, ${item_number})`)
  reset_editor(editor_number);  // unselect all the items
    
    console.log('given item num.', item_number);
    
    // Display selected item (code/file)
    console.log('display_block::codePreview_' + editor_number + '_' + item_number);
    document.getElementById('codePreview_' + editor_number + '_' + item_number).style.display = "block";

    // Color of selected sidebar item
    console.log('background_black::sidebar_code_' + editor_number + '_' + item_number);
    document.getElementById('sidebar_code_' + editor_number + '_' + item_number).style.background='black';
}

function preview_file(editor_number, item_number) {
  console.log(`invoked: preview_file(${editor_number}, ${item_number})`)
  reset_editor(editor_number);  // unselect all the items
  
  // Display selected file
  console.log('display_block::filePreview_' + editor_number + '_' + item_number);
  document.getElementById('filePreview_' + editor_number + '_' + item_number).style.display = "block";

  // Color of selected sidebar file
  console.log('background_black::sidebar_file_' + editor_number + '_' + item_number);
  document.getElementById('sidebar_file_' + editor_number + '_' + item_number).style.background='black';
}
  

//s  Form to add new code to an editor
function add_code_to_editor(editor_number){
  console.log(`add_files_(${editor_number})`)
  reset_editor(editor_number);  // unselect all the items
  
  // Display sidebar item
  document.getElementById('sidebar_code_' + editor_number + '_0').style.display = "block";
  
  // color the sidebar item: 'New Files' black
  document.getElementById('sidebar_code_' + editor_number + '_0').style.background = "black";

  // Display the code form
  document.getElementById('codePreview_' + editor_number + '_0').style.display = "block";
}



function add_files_to_editor(editor_number){
  // add file form to individual editor
  // hide all the children of display area
  // display the file form
  // add the sidebar item
  // color the sidebar item black
  console.log(`add_files_(${editor_number})`)
  reset_editor(editor_number);  // unselect all the items

  // Display sidebar item
  document.getElementById('sidebar_file_' + editor_number + '_0').style.display = "block";
  
  
  // color the sidebar item: 'New Files' black
  document.getElementById('sidebar_file_' + editor_number + '_0').style.background = "black";
/*
on click upload show loader and disable the button
hide on file upload success/error
on file upload, add more sidebar items and their corresponding display areas
*/

  // Display the file form
  document.getElementById('filePreview_' + editor_number + '_0').style.display = "block";
}


// Function to toggle full screen mode
function toggleFullscreen(editor_number) {
  // Get the element that we want to take into fullscreen mode
  let fullscreenElement = document.getElementById('editor-' + editor_number);
  if (document.fullscreenElement ||
      document.mozFullScreenElement || // Firefox
      document.webkitFullscreenElement || // Chrome, Safari, and Opera
      document.msFullscreenElement // IE/Edge
  ) {
      // If in full screen, exit full screen
      if (document.exitFullscreen) {
          document.exitFullscreen();
      } else if (document.mozCancelFullScreen) {
          document.mozCancelFullScreen(); // Firefox
      } else if (document.webkitExitFullscreen) {
          document.webkitExitFullscreen(); // Chrome, Safari, and Opera
      } else if (document.msExitFullscreen) {
          document.msExitFullscreen(); // IE/Edge
      }
  } else {
      // If not in full screen, request full screen
      if (fullscreenElement.requestFullscreen) {
          fullscreenElement.requestFullscreen();
      } else if (fullscreenElement.mozRequestFullScreen) {
          fullscreenElement.mozRequestFullScreen(); // Firefox
      } else if (fullscreenElement.webkitRequestFullscreen) {
          fullscreenElement.webkitRequestFullscreen(); // Chrome, Safari, and Opera
      } else if (fullscreenElement.msRequestFullscreen) {
          fullscreenElement.msRequestFullscreen(); // IE/Edge
      }
  }
}




function copy_to_clipboard (editor_number, item_number) {
  // Get the code block element
  var codeBlock = document.getElementById('codePreview_' + editor_number+'_'+item_number);

  // Create a range to select the text inside the code block
  var range = document.createRange();
  range.selectNode(codeBlock);

  // Add the range to the clipboard
  var selection = window.getSelection();
  selection.removeAllRanges();
  selection.addRange(range);

  // Execute the copy command
  document.execCommand('copy');

  // Clean up the selection
  selection.removeAllRanges();

  // Notify the user that the code has been copied (optional)
  alert('Code has been copied to the clipboard!');
}