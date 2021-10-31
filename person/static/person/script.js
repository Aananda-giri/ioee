/*
<!-- ############### Redundant Code ####################### -->
<!-- ############### For getting profile details again ########## -->
    <form id="getprofile" action="/profile/" method="POST">
      {% csrf_token %}
        
      <input type="checkbox" name="last_name" value="{{person.last_name}}" style="opacity:0;" checked>
      <input type ="checkbox" name="first_name" value = "{{person.first_name}}" style="opacity:0;" checked>{{each_category}}</input>
      
    </form>
*/
function appendSearchResults(person,i){
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
  img.setAttribute('src', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS52y5aInsxSm31CvHOFHWujqUx_wWTS9iM6s7BAm21oEN_RiGoog');
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
