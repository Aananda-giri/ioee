/*Deadlock between display_image function, image html code while calling display_image function */
var collages = ['PUL', 'THA', 'PAS', 'PUR', 'KAT', 'KAN', 'SEC', 'ACE', 'HCE', 'NCE', 'LEC', 'KIC', 'JAN', 'KEC', 'CHI']

var collage_faculties = [['BCE', 'BCT', 'BEI', 'BEL', 'BAR', 'BCH', 'BME'], ['BCE', 'BCT', 'BEI', 'BAR', 'BME', 'BIE', 'BAM'], ['BCE', 'BCT', 'BEI', 'BEL', 'BAM', 'BME', 'BGE'], ['BCE', 'BCT', 'BEI', 'BEL', 'BAR', 'BME', 'BAG'], ['BCE', 'BCT', 'BEI', 'BEL', 'BAR'], ['BCE', 'BCT', 'BEI'], ['BCE', 'BCT', 'BEI'], ['BCE', 'BCT', 'BEI', 'BEL'], ['BCE', 'BCT', 'BEI', 'BAR'], ['BCE', 'BCT', 'BEI', 'BEL'], ['BCE', 'BCT'], ['BCE', 'BCT', 'BEI'], ['BCE', 'BCT', 'BEI'], ['BCE', 'BCT', 'BEL'], ['BAR']]

var faculties = ['BCE', 'BCT', 'BEI', 'BAR', 'BME', 'BEL', 'BCH', 'BIE', 'BAM', 'BGE', 'BAG',]

var students = [[192, 96, 48, 48, 48, 48, 48], [144, 48, 48, 48, 48, 48, 48], [144, 48, 48, 48, 48, 48, 48], [96, 96, 48, 48, 48, 96, 48], [96, 96, 96, 48, 48], [96, 96, 96], [48, 48, 48], [96, 96, 96, 48], [96, 48, 48, 48], [96, 48, 48, 48], [48, 48], [96, 48, 48], [96, 48, 48], [96, 48, 48], [24]]





function ultimate_function(gender){
console.log('got gender: ' + gender)  
}

function get_gender(gender){
console.log('got gender: ' + gender)  

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








function showMessage(message){
console.log('\n\n\nError Message : ' +message);
}




function toggleDisplay(id, element=false){
//to toggle display of any element
  if (element){
    element=id;
  } else{
  
    element = document.getElementById(id);
  }
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



function displayPhotos(profile_pic){
  document.getElementById('profile_pic_div').style.display='block';
}

function getSrc(){
return('https://wallpapercave.com/wp/wp4997652.jpg')
}





function read(){
var reader = new FileReader((function(self) {
    return function(e) {
      document.getElementById("img").src = e.target.result;
    }
  })(this))};







function getBase64Image(img) {
  var canvas = document.createElement("canvas");
  canvas.width = img.width;
  canvas.height = img.height;
  var ctx = canvas.getContext("2d");
  ctx.drawImage(img, 0, 0);
  var dataURL = canvas.toDataURL(img.src);
  return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
}
function base64(){
  var base64 = getBase64Image(document.getElementById("imageid"));

  img=document.createElement('img')
  img.setAttribute('src', base64)
  document.body.appendChild(img);
}


function getSrc(){
return("https://i.pinimg.com/originals/b7/d7/1c/b7d71cec933bdee0553f552481f25d02.jpg")
}
var canvas = document.createElement("canvas");
context = canvas.getContext('2d');

make_base();

function make_base()
{
  base_image = new Image();
  base_image.src = "https://i.pinimg.com/originals/b7/d7/1c/b7d71cec933bdee0553f552481f25d02.jpg";
  base_image.onload = function(){
    context.drawImage(base_image, 100, 100);
  }
}

function mage_base(){
var jpgUrl = canvas.toDataURL("image/jpg");
img=document.createElement('img');
img.setAttribute('src',jpgUrl);
document.body.appendChild(img);}

function getFaculties(){
  let faculty_div = document.getElementById("select_faculty_options");
  if(faculty_div.childNodes.length<14){
    for (faculty of faculties){
      let faculty_option = document.createElement('option');
      faculty_option.setAttribute('onClick','collage_faculty_details()');
      faculty_option.textContent = faculty;
      faculty_div.appendChild(faculty_option);
    }
  }
}

function getCollages(){
  let collage_div = document.getElementById("select_collage_options");
  if(collage_div.childNodes.length<20){
    for (collage of collages.sort().reverse()){
      let collage_option = document.createElement('option');
      collage_option.setAttribute('onClick', 'collage_faculty_details()');
      collage_option.textContent = collage;
      collage_div.appendChild(collage_option);
    }
  }
}

function display_pics(random_pairs, url_base='', ioe_roll_no='', round_value='', round_id=''){
  
console.log('random_pairs'+random_pairs);
console.log('url_base'+url_base);
console.log('ioe_roll_no'+ioe_roll_no);
console.log('round_value'+round_value);
console.log('round_id'+round_id);

}



function create_image_divs(){
  
  let container = document.createElement('div');
  container.setAttribute('class', 'row');
  
  let div1 = document.createElement('div');
  div1.setAttribute('class','col-lg-6 img-responsive mb-2');
  
  let img1 = document.createElement('img');
    img1.setAttribute('onClick', "vote_image(1)");
    img1.setAttribute('id', "first_image");
    img1.setAttribute('class','mb-2');
    img1.setAttribute('style', "height:50vh;");
    img1.setAttribute('class', "bg;");
    img1.setAttribute('onerror', "");/*window.location.reload(true);*/
  let br = document.createElement('br')
  div1.appendChild(img1);
  div1.appendChild(br);
  container.appendChild(div1);
    
  
  let div2 = document.createElement('div');
    div2.setAttribute('class','col-lg-6 img-responsive mt-2');
  
  let img2 = document.createElement('img');
    img2.setAttribute('onClick', "vote_image(2)");
    img2.setAttribute('id', "second_image");
    img2.setAttribute('class','mt-2');
    img2.setAttribute('style', "height:50vh;");
    img2.setAttribute('onerror', ");");
  div2.appendChild(img2);
  container.appendChild(div2);
  
  document.body.appendChild(container);
  
}


