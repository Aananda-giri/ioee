function createEditor(key, i){
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
    </h2>
    <div
      id="collapse${i}"
      class="accordion-collapse collapse show"
      aria-labelledby="heading${i}"
      data-bs-parent="#accordionExample"
      >
      <div class="accordion-body editor">
        <div class='editor__code'id="editor${i}"></div>
      </div>
    </div>
  </div>`;
}
function setupEditor(key,i) {
  
  //for (key in codes) {
    window.editor = ace.edit(`editor${i}`);
    editor.setTheme("ace/theme/one_dark");
    editor.getSession().setMode("ace/mode/c_cpp");
    editor.setValue(key.code, 1); //1 = moves cursor to end

    editor.setReadOnly(true);
    editor.setOptions({
      fontSize: "16pt",
      showLineNumbers: true,
      showGutter: true,
      // vScrollBarAlwaysVisible: true,
    });
  //}
}
//setupEditor();

function okSetupEditor(codes) {
  var i=1;
  for (code of codes){
    // console.log(code['fields']['title']);
    // code['fields']['author'];
    // code['fields']['created_on'];
    //console.log(code['fields']['code']);
    //console.log(code['fields']['created_on']);
    var well_formatted_code = {
      id: i,
      author: code['fields']['author'],
      title: code['fields']['title'],
      timestamp: code['fields']['created_on'],
      code: code['fields']['code'],
    }
    createEditor(well_formatted_code, i);
    setupEditor(well_formatted_code,i);
    i= i+1;

  /*console.log(codes);
  console.log(codes[0]);
  console.log(codes[0].fields['code']);
  console.log(codes[0]['fields']);*/

    //console.log(code['code']);
    //console.log(code.['fields']['code']);
    //created_on = codefields['created_on'];
    //title = code.fields['title'];
    /*
    window.editor = ace.edit(`editor${code}`);
    editor.setTheme("ace/theme/one_dark");
    editor.getSession().setMode("ace/mode/c_cpp");
    //editor.setValue(key.code, 1); //1 = moves cursor to end
    editor.setValue(code);

    editor.setReadOnly(true);
    editor.setOptions({
      fontSize: "16pt",
      showLineNumbers: true,
      showGutter: true,
      // vScrollBarAlwaysVisible: true,
    });*/
  }
  // document.write('hi')
  // document.write(code);
};
//okSetupEditor();
