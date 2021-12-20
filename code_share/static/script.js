function editCode(code_position) {
  
  console.log(code_position);
  var parent_code_id = dataa[code_position].pk;
  url = window.location.origin + '/edit/'+parent_code_id+'/';
  window.location.href = url;
  //onClick="editCode('${i-1}')"
}
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
  copy_btn = document.getElementById('copy' + code_position);
  copy_btn.style.backgroundColor='#00FF00';
  copy_btn.style.color='white';
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
        <h4><b>${key.title}</b></h4>
      </div>
      </i>
      <div class="accordion-right-title">
        <h5><b>${key.author}</b></h5>
        <h5>${key.timestamp}</h5>
      </div>
    </div>
    
  </button>
  <i class="accordion-item my-3 position-absolute copy far fa-copy" id="copy${i-1}" onClick="copyToClipboard('${i-1}')">
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
    <div class='editor__code 'id="editor${i}"></div>
  </div>
  </div>

    <!-- For Edit code footer-->
    <div class="m-2 d-flex" style="color: white; ">
      <div style="width: 6vw;cursor: pointer;background-color: green" class="fw-bold fst-italic branch_footer rounded text-center">
        main
      </div>
      <div style="width: 6vw;cursor: pointer;background-color: #282C34;" class="fw-bold rounded text-center ms-2" onClick="editCode('${i-1}')">
        add_branch
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
    };
    createEditor(well_formatted_code, i);
    // setupEditor(well_formatted_code);
    i = i + 1;
  }
}
