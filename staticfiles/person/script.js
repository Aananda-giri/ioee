// disables left click on page
document.onkeydown = function(e) {
    //source:https://stackoverflow.com/questions/6597224/how-to-hide-html-source-disable-right-click-and-text-copy
    if(e.keyCode == 123) {
     return false;  //f12 disabled
    }
    if(e.ctrlKey && e.shiftKey && e.keyCode == 'I'.charCodeAt(0)){
     return false;
    }
    if(e.ctrlKey && e.shiftKey && e.keyCode == 'J'.charCodeAt(0)){
     return false;
    }
    if(e.ctrlKey && e.keyCode == 'U'.charCodeAt(0)){
     return false;
    }

    if(e.ctrlKey && e.shiftKey && e.keyCode == 'C'.charCodeAt(0)){
     return false;
    }      
 }
// disables right click
document.addEventListener('contextmenu', event => event.preventDefault());


var collages = ['PUL', 'THA', 'PAS', 'PUR', 'KAT', 'KAN', 'SEC', 'ACE', 'HCE', 'NCE', 'LEC', 'KIC', 'JAN', 'KEC', 'CHI']

var collage_faculties = [['BCE', 'BCT', 'BEI', 'BEL', 'BAR', 'BCH', 'BME'], ['BCE', 'BCT', 'BEI', 'BAR', 'BME', 'BIE', 'BAM'], ['BCE', 'BCT', 'BEI', 'BEL', 'BAM', 'BME', 'BGE'], ['BCE', 'BCT', 'BEI', 'BEL', 'BAR', 'BME', 'BAG'], ['BCE', 'BCT', 'BEI', 'BEL', 'BAR'], ['BCE', 'BCT', 'BEI'], ['BCE', 'BCT', 'BEI'], ['BCE', 'BCT', 'BEI', 'BEL'], ['BCE', 'BCT', 'BEI', 'BAR'], ['BCE', 'BCT', 'BEI', 'BEL'], ['BCE', 'BCT'], ['BCE', 'BCT', 'BEI'], ['BCE', 'BCT', 'BEI'], ['BCE', 'BCT', 'BEL'], ['BAR']]

var faculties = ['BCE', 'BCT', 'BEI', 'BAR', 'BME', 'BEL', 'BCH', 'BIE', 'BAM', 'BGE', 'BAG',]

var students = [[192, 96, 48, 48, 48, 48, 48], [144, 48, 48, 48, 48, 48, 48], [144, 48, 48, 48, 48, 48, 48], [96, 96, 48, 48, 48, 96, 48], [96, 96, 96, 48, 48], [96, 96, 96], [48, 48, 48], [96, 96, 96, 48], [96, 48, 48, 48], [96, 48, 48, 48], [48, 48], [96, 48, 48], [96, 48, 48], [96, 48, 48], [24]]

year = [73,74,75,76]

/*
<!-- ############### Redundant Code ####################### -->
<!-- ############### For getting profile details again ########## -->
    <form id="getprofile" action="/profile/" method="POST">
      {% csrf_token %}
        
      <input type="checkbox" name="last_name" value="{{person.last_name}}" style="opacity:0;" checked>
      <input type ="checkbox" name="first_name" value = "{{person.first_name}}" style="opacity:0;" checked>{{each_category}}</input>
      
    </form>
*/
function appendSearchResults(person,i, url){
  document.getElementById('adding_form').style.display="none";
  
  let form = document.createElement('form');
  form.setAttribute('id', 'getprofile'+i);
  form.setAttribute('method', 'GET');
  form.setAttribute('action', '/profile/');
  document.body.appendChild(form);
  
  let in1 = document.createElement('input');
  in1.setAttribute('type', 'checkbox');
  in1.setAttribute('name', 'last_name');
  in1.setAttribute('value', String(person.last_name));
  in1.setAttribute('style', 'opacity:0;');
  in1.setAttribute('checked', 'true');
  form.appendChild(in1);
  
  let in2 = document.createElement('input');
  in2.setAttribute('type', 'checkbox');
  in2.setAttribute('name', 'first_name');
  in2.setAttribute('value', String(person.first_name));
  in2.setAttribute('style', 'opacity:0;');
  in2.setAttribute('checked', 'true');
  form.appendChild(in2);





  let container = document.createElement('div');
  container.setAttribute('class', 'container emp-profile');
  container.setAttribute('type', 'submit');
  let action='document.getElementById("getprofile").submit();'
  container.setAttribute('onClick',action.slice(0,35)+i+action.slice(35) );
  document.body.appendChild(container);


  let img = document.createElement('img');
  img.setAttribute('class', 'img-fluid float-left img-responsive mr-2 md-6 rounded-circle');
  img.setAttribute('width', '200');
  img.setAttribute('src', String(url));
  img.setAttribute('alt', '');
  container.appendChild(img);
  
  
  h3 = document.createElement('h3');
  container.appendChild(h3);
  
  
  //person=document.createElement("{{person.first_name.title}} {{ person.middle_name.title }} {{ person.last_name.title }}");
  //h3.appendChild(person);
  h3.textContent= String(person.first_name) +' '+ String(person.middle_name) + ' ' +  String(person.last_name);
  
  strong = document.createElement('strong');
  container.appendChild(strong);
  
  //profession = document.createElement("Proefession : {{ person.profession }}");
  //strong.appendChild(profession);
  
  strong.textContent = "Proefession : " +person.profession;
  br = document.createElement('br');
  strong.appendChild(br);
  
  //education = document.createElement("Education : {{ person.education.0.title }}");
  //strong.appendChild(education);
  
  strong2 = document.createElement('strong');
  container.appendChild(strong2);
  strong2.textContent = "Education : " + person.education;
  

  //profession.appendChild(br);
}
/*



<div class="container emp-profile" type="submit" onClick="document.getElementById('getprofile').submit();">
  <img  class="img-fluid mr-3 float-left img-responsive mr-2 md-6 rounded-circle" width=200 src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS52y5aInsxSm31CvHOFHWujqUx_wWTS9iM6s7BAm21oEN_RiGoog" alt=""/>

  
  <h3>{{ person.first_name.title }} {{ person.middle_name.title }} {{ person.last_name.title }}</h3> <br>
  
  <strong>
  Proefession : {{ person.profession }}<br>
    
  Education : {{ person.education.0.title }}
      
  </strong><br>


</div>


*/


function showMessage(message){
console.log('\n\n\nError Message : ' +message);
}

//to toggle display of any element
function toggleDisplay(id){
  element = document.getElementById(id);
  if (element.style.display == "block"){
    element.style.display = "none";
    //console.log(0)
  } else{
    //console.log(element);
    element.style.display = "block";
    //console.log(1);
    //console.log(element);
  }
  
}

function showAddingTab(really=true){
  if (really){
    show = "block";
    hide = "none";
  } else {    show = "none";
              hide = "block";}
  document.getElementById('adding_form').style.display=show;
  document.querySelector('.container').style.display=hide;
  document.getElementById('add_button').style.display=hide;
  document.getElementById('profile_pic_div').style.display='none';

}

function displayPhotos(profile_pic){
  document.getElementById('profile_pic_div').style.display='block';
}



function create_collage_dropdowns(){
  let main_div = document.getElementById('droprignt_collage_div');
  let br = document.createElement('br');
  
  for (const [index, collage] of collages.entries()){
  
    let button = document.createElement('button');
      button.setAttribute("class", "btn btn-success dropdown-toggle");
      button.setAttribute("type", "button");
      button.setAttribute("id", "dropdownMenuButton");
      button.setAttribute("data-toggle", "dropdown");
      button.setAttribute("aria-haspopup", "true");
      button.setAttribute("aria-expanded", "false");
      button.textContent = collage;
  
    main_div.appendChild(br);
    main_div.appendChild(button);
  
    let each_collage_div = document.createElement('div');
      each_collage_div.setAttribute("class", "dropdown-menu");
      each_collage_div.setAttribute("aria-labelledby", "dropdownMenuButton");
  
    for (faculty of faculties[index]){
  
    let a = document.createElement('a');
      a.setAttribute('class', 'dropdown-item');
      a.setAttribute('href', '/collage/' + collage + '/' + faculty);
      each_collage_div.appendChild(a);
  
  
  main_div.appendChild(each_collage_div);}}
}

function toggle_spinner(){
  if (document.getElementById('floating_spinner').style.display=='none'){
    document.getElementById('floating_spinner').style.display='block';
  } else{document.getElementById('floating_spinner').style.display='none';}
  
}
