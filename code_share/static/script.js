function copyToClipboard(code_position) {
  console.log(code_position);
  var text = dataa[code_position].fields.code;
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
  <i class="accordion-item my-3 position-absolute" id="copy${i}" onClick="copyToClipboard('${i}')"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clipboard" viewBox="0 0 16 16">
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
