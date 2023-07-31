# ioee :: no-login code sharing site with nice template
<B><i>Introduction:</i></b>

live_website : https://ioee.herokuapp.com/


editor:
 - currently using: ace editor
 - to change to : code mirror 6
 references: 
 https://blog.replit.com/code-editors
 https://codemirror.net/6/docs/
 https://dyclassroom.com/codemirror/how-to-setup-codemirror



bulk create files
bulk create codes
post file, code
* code_share.home2 -> alert if file is empty before upload

## Yet to do:
* code color theme
* debug broken css of eeditor on include to home2.html
* code_share/home2/pagination
code_share.models.Files::
    remove: link, download_link :: use file_id only
code_share.editor.html::
    image preview in gallery like view: (left/right) arrow keys to navigate within images of same container
code_share.editor.html.file_upload::
    preview before upload
code_share.editor.html.file_upload.success::
    success bootstrap notice
