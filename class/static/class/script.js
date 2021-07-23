var collages = ['PUL', 'THA', 'PAS', 'PUR', 'KAT', 'KAN', 'SEC', 'ACE', 'HCE', 'NCE', 'LEC', 'KIC', 'JAN', 'KEC', 'CHI']

var collage_faculties = [['BCE', 'BCT', 'BEI', 'BEL', 'BAR', 'BCH', 'BME'], ['BCE', 'BCT', 'BEI', 'BAR', 'BME', 'BIE', 'BAM'], ['BCE', 'BCT', 'BEI', 'BEL', 'BAM', 'BME', 'BGE'], ['BCE', 'BCT', 'BEI', 'BEL', 'BAR', 'BME', 'BAG'], ['BCE', 'BCT', 'BEI', 'BEL', 'BAR'], ['BCE', 'BCT', 'BEI'], ['BCE', 'BCT', 'BEI'], ['BCE', 'BCT', 'BEI', 'BEL'], ['BCE', 'BCT', 'BEI', 'BAR'], ['BCE', 'BCT', 'BEI', 'BEL'], ['BCE', 'BCT'], ['BCE', 'BCT', 'BEI'], ['BCE', 'BCT', 'BEI'], ['BCE', 'BCT', 'BEL'], ['BAR']]

var faculties = ['BCE', 'BCT', 'BEI', 'BAR', 'BME', 'BEL', 'BCH', 'BIE', 'BAM', 'BGE', 'BAG']

var students = [[192, 96, 48, 48, 48, 48, 48], [144, 48, 48, 48, 48, 48, 48], [144, 48, 48, 48, 48, 48, 48], [96, 96, 48, 48, 48, 96, 48], [96, 96, 96, 48, 48], [96, 96, 96], [48, 48, 48], [96, 96, 96, 48], [96, 48, 48, 48], [96, 48, 48, 48], [48, 48], [96, 48, 48], [96, 48, 48], [96, 48, 48], [24]]

years = [73,74,75,76]




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

function getYears(){
  let year_div = document.getElementById("select_year_options");
  if(year_div.childNodes.length<4){
    for (year of years.sort().reverse()){
      let year_option = document.createElement('option');
      year_option.setAttribute('onClick', 'collage_faculty_details()');
      year_option.textContent = year;
      year_div.appendChild(year_option);
    }
  }
}
