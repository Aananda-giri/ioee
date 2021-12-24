function copyToClipboard(code_position) {
  console.log(code_position);
  var text = dataa[code_position].fields.code;
  console.log(text);
  var dummy = document.createElement("textarea");
  // to avoid breaking orgain page when copying more words
  // cant copy when adding below this code
  // dummy.style.display = 'none'
  document.body.appendChild(dummy);
  //Be careful if you use texarea. setAttribute('value', value), which works with "input" does not work with "textarea". – Eduard
  dummy.value = text;
  dummy.select();
  document.execCommand("copy");
  document.body.removeChild(dummy);
  //.style.backgroundColor='#00FF00'
  copy_btn = document.getElementById("copy" + code_position);
  copy_btn.style.backgroundColor = "#00FF00";
  copy_btn.style.color = "white";
}

function createEditor(key, i) {
  //for (key in codes) {

  let accordion = document.getElementById("accordionExample");
  accordion.innerHTML += `
<div class="accordion-item my-3">
  <h2 class="accordion-header" id="heading${i}">
    <button
      class="accordion-button"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#collapse${i}"
      aria-expanded="true"
      aria-controls="collapse${i}"
    >
    <div class="accordion-title">
      <div class="accordion-left-title">
        <h4>${key.title}</h4>
      </div>
      <div class="accordion-right-title">
        <h5>${key.author}</h5>
        <h5>${key.timestamp}</h5>
      </div>
    </div>
    </button>
    <i
    id="collapse${i}"
    
    class="accordion-item my-3 position-absolute  collapse show copy far fa-copy" id="copy${
      i - 1
    }" onClick="copyToClipboard('${i - 1}')">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clipboard" viewBox="0 0 16 16">
        <path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"/>
        <path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3z"/>
      </svg>
      </i>
  </h2>

  <div
    id="collapse${i}"
    class="accordion-collapse collapse show"
    aria-labelledby="heading${i}"
  
    >
    <div class="accordion-body editor">
      <div class='editor__code'id="editor${i}">
      </div>
    </div> 
    <!-- For Edit code footer-->
      <div id = "branches_${key.pk}" class="m-2 d-flex" style="color: white; ">
        
        <div id="main${i}" style="width: 6vw;cursor: pointer;background-color: green" class="fw-bold fst-italic branch_footer rounded text-center" onClick="toggleCodeView(${i},${-1});">
          main
        </div>

        <div id="edit${i}" style="width: 6vw;cursor: pointer;background-color: #282C34;" class="fw-bold rounded text-center ms-2"
        onClick="editCoder(${i})"
        >
          edit
        </div>

        <div id="star${
          i - 1
        }" style="width: 6vw;cursor: pointer;background-color: #282C34;" class="fw-bold rounded text-center ms-2" onClick="starCode(${
    i - 1
  })">
          stars(${key.stars})
        </div>
        <div id="save${i}" style="width: 6vw;cursor: pointer;background-color: #282C34;" class="save fw-bold rounded text-center ms-2" onClick="save(${i})">
          Save
        </div>

      </div>
</div>`;
  //}
}

function setupEditor(codes) {
  let i = 1;
  for (key of codes) {
    window.editor = ace.edit(`editor${i}`);
    editor.setTheme("ace/theme/one_dark");
    editor.getSession().setMode("ace/mode/c_cpp");
    editor.setValue(key["fields"]["code"], 1); //1 = moves cursor to end

    editor.setReadOnly(true);
    editor.setOptions({
      fontSize: "16pt",
      showLineNumbers: true,
      showGutter: true,
    });

    i++;
  }
}

function okSetupEditor(codes) {
  console.log("codes", codes);
  var i = 1;
  for (code of codes) {
    var well_formatted_code = {
      id: i,
      author: code["fields"]["author"],
      title: code["fields"]["title"],
      timestamp: code["fields"]["created_on"],
      code: code["fields"]["code"],
      stars: code["fields"]["stars"],
      pk: code.pk,
    };
    createEditor(well_formatted_code, i);
    // setupEditor(well_formatted_code);
    i = i + 1;
  }
}
function editCoder(i) {
  window.editor = ace.edit(`editor${i}`);
  editor.getValue();
  editor.setReadOnly(false);
  let saveCode = document.getElementById(`save${i}`);
  saveCode.style.display = "block";
}

function displayCode(i){
  window.editor = ace.edit(`editor${i}`);
  if (what=='main')
    editor.setValue(dataa[i-1]["fields"]["code"], 1); 
    //get branch_datas
    else{
    editor.setValue(dataa[i-1]["fields"]["code"], 1); 
  }
}

function toggleCodeView(code_index, branch_index){
  console.log(code_index);
  console.log('branch_index:');
  console.log(branch_index);
  window.editor = ace.edit(`editor${code_index}`);
  if (branch_index==-1){
    //for main branch: branch_index=-1
    console.log('\nbranch-1\n');
    editor.setValue(dataa[code_index-1].fields.code, 1); //1 = moves cursor to end
  } else {
    //branch code to be displayed
    editor.setValue(branches[branch_index].fields.code, 1); //1 = moves cursor to end
  }



}

function distributeBranch(branch_data, branch_index){
  console.log(branch_data);
  let branches_parent_div = document.getElementById('branches_' + branch_data.Parent);
  
  let branches_div = document.createElement('div');
  let p = parseInt(branches_parent_div.parentNode.id.split('collapse')[1]); //position count of div within page

  branches_div.setAttribute('class', 'fw-bold rounded text-center ms-2');
  
  branches_div.setAttribute('id', 'branch' + p);
  branches_div.setAttribute('style', 'width: 6vw;cursor: pointer;background-color: #282C34;');
  branches_div.setAttribute('class', 'fw-bold rounded text-center ms-2');
  branches_div.setAttribute('onClick', `toggleCodeView(${parseInt(p)}, ${branch_index} )`);
  branches_div.textContent = `branch(${branch_index})`;
  branches_parent_div.appendChild(branches_div);
}