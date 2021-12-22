function editCode(code_position) {
  
  console.log(code_position);
  var parent_code_id = dataa[code_position].pk;
  url = window.location.origin + '/edit/'+parent_code_id+'/';
  window.location.href = url;
  // onClick="editCode('${i-1}')"
  // <input type="text" placeholder="title"></input>
  // <input type="text" placeholder="author"></input>
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
        edit
      </div>
      
      <div id="star${i-1}" style="width: 6vw;cursor: pointer;background-color: #282C34;" class="fw-bold rounded text-center ms-2" onClick="starCode('${i-1}')">
        stars(${key.stars})
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
    };
    createEditor(well_formatted_code, i);
    // setupEditor(well_formatted_code);
    i = i + 1;
  }
}







//readonly=""
// read only
// <div class="accordion-item my-3">
//   <h2 class="accordion-header" id="heading1">
//   <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse1" aria-expanded="true" aria-controls="collapse1">
//     <div class="accordion-title">
//       <div class="accordion-left-title">
//         <h4><b>stick</b></h4>
//       </div>
      
//       <div class="accordion-right-title">
//         <h5><b>me</b></h5>
//         <h5>2021-12-20T13:14:17.088Z</h5>
//       </div>
//     </div>
    
//   </button>
//   <i class="accordion-item my-3 position-absolute copy far fa-copy" id="copy0" onclick="copyToClipboard('0')">
//   <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clipboard" viewBox="0 0 16 16">
//   <path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"></path>
//   <path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3z"></path>
// </svg> 
// </i>
//   </h2>
//   <div id="collapse1" class="accordion-collapse collapse show" aria-labelledby="heading1">
//   <div class="accordion-body editor">
//     <div class="editor__code ace_editor ace_hidpi ace-one-dark ace_dark" id="editor1" style="font-size: 16pt;"><textarea class="ace_text-input" autocorrect="off" autocapitalize="off" spellcheck="false" style="opacity: 0; font-size: 1px; height: 1px; width: 1px; transform: translate(204px, 26px);" wrap="off"></textarea><div class="ace_gutter" aria-hidden="true" style="left: 0px; width: 46px;"><div class="ace_layer ace_gutter-layer ace_folding-enabled" style="height: 1000000px; transform: translate(0px); width: 46px;"><div class="ace_gutter-cell ace_gutter-active-line " style="height: 26px; top: 0px;">1<span style="display: none;"></span></div></div></div><div class="ace_scroller" style="line-height: 26px; left: 46px; right: 0px; bottom: 0px;"><div class="ace_content" style="transform: translate(0px); width: 706px; height: 234px;"><div class="ace_layer ace_print-margin-layer"><div class="ace_print-margin" style="left: 1031px; visibility: visible;"></div></div><div class="ace_layer ace_marker-layer"><div style="height: 26px; top: 0px; left: 0px; right: 0px;" class="ace_active-line"></div></div><div class="ace_layer ace_text-layer" style="height: 1000000px; margin: 0px 4px; transform: translate(0px);"><div style="height: 26px; top: 0px;" class="ace_line"><span class="ace_identifier">hello</span> <span class="ace_identifier">Worldh</span></div></div><div class="ace_layer ace_marker-layer"></div><div class="ace_layer ace_cursor-layer ace_hidden-cursors"><div class="ace_cursor" style="display: block; transform: translate(158px); width: 13px; height: 26px; animation-duration: 1000ms;"></div></div></div></div><div class="ace_scrollbar ace_scrollbar-v" style="display: none; width: 17px; bottom: 0px;"><div class="ace_scrollbar-inner" style="width: 17px; height: 26px;">&nbsp;</div></div><div class="ace_scrollbar ace_scrollbar-h" style="display: none; height: 17px; left: 46px; right: 0px;"><div class="ace_scrollbar-inner" style="height: 17px; width: 706px;">&nbsp;</div></div><div style="height: auto; width: auto; top: 0px; left: 0px; visibility: hidden; position: absolute; white-space: pre; font: inherit; overflow: hidden;"><div style="height: auto; width: auto; top: 0px; left: 0px; visibility: hidden; position: absolute; white-space: pre; font: inherit; overflow: visible;">הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה</div><div style="height: auto; width: auto; top: 0px; left: 0px; visibility: hidden; position: absolute; white-space: pre; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; font-size-adjust: inherit; font-kerning: inherit; font-optical-sizing: inherit; font-language-override: inherit; font-feature-settings: inherit; font-variation-settings: inherit; overflow: visible;">XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX</div></div></div>
//   </div>
//   </div>

//     <!-- For Edit code footer-->
//     <div class="m-2 d-flex" style="color: white; ">
//       <div style="width: 6vw;cursor: pointer;background-color: green" class="fw-bold fst-italic branch_footer rounded text-center">
//         main
//       </div>
//       <div style="width: 6vw;cursor: pointer;background-color: #282C34;" class="fw-bold rounded text-center ms-2" onclick="editCode('0')">
//         edit
//       </div>
//     </div>
  
//   </div>




// editable
// <div class="accordion-item my-3">
//   <h2 class="accordion-header" id="heading2">
//   <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse2" aria-expanded="true" aria-controls="collapse2">
//     <div class="accordion-title">
//       <div class="accordion-left-title">
//         <h4><b>PLUTO</b></h4>
//       </div>
      
//       <div class="accordion-right-title">
//         <h5><b>PLUTO</b></h5>
//         <h5>2021-12-15T10:16:51.047Z</h5>
//       </div>
//     </div>
    
//   </button>
//   <i class="accordion-item my-3 position-absolute copy far fa-copy" id="copy1" onclick="copyToClipboard('1')">
//   <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clipboard" viewBox="0 0 16 16">
//   <path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"></path>
//   <path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3z"></path>
// </svg> 
// </i>
//   </h2>
//   <div id="collapse2" class="accordion-collapse collapse show" aria-labelledby="heading2">
//   <div class="accordion-body editor">
//     <div class="editor__code ace_editor ace_hidpi ace-one-dark ace_dark" id="editor2" style="font-size: 16pt;"><textarea class="ace_text-input" autocorrect="off" autocapitalize="off" spellcheck="false" style="opacity: 0; font-size: 1px; transform: translate(63px, 122px); height: 1px; width: 1px;" readonly="" wrap="off"></textarea><div class="ace_gutter" aria-hidden="true" style="left: 0px; width: 59px;"><div class="ace_layer ace_gutter-layer ace_folding-enabled" style="height: 1000000px; transform: translate(0px, -60px); width: 59px;"><div class="ace_gutter-cell " style="height: 26px; top: 52px;">3<span style="display: none;"></span></div><div class="ace_gutter-cell " style="height: 26px; top: 78px;">4<span style="display: none;"></span></div><div class="ace_gutter-cell " style="height: 26px; top: 104px;">5<span style="display: none;"></span></div><div class="ace_gutter-cell " style="height: 26px; top: 130px;">6<span style="display: none;"></span></div><div class="ace_gutter-cell ace_gutter-active-line " style="height: 26px; top: 156px;">7<span style="display: none;"></span></div><div class="ace_gutter-cell " style="height: 26px; top: 182px;">8<span style="display: none;"></span></div><div class="ace_gutter-cell " style="height: 26px; top: 208px;">9<span style="display: inline-block; height: 26px;" class="ace_fold-widget ace_start ace_open"></span></div><div class="ace_gutter-cell " style="height: 26px; top: 234px;">10<span style="display: none;"></span></div><div class="ace_gutter-cell " style="height: 26px; top: 260px;">11<span style="display: none;"></span></div></div></div><div class="ace_scroller" style="line-height: 26px; left: 58.6641px; right: 12px; bottom: 0px;"><div class="ace_content" style="transform: translate(0px, -8px); width: 1086px; height: 222px;"><div class="ace_layer ace_print-margin-layer"><div class="ace_print-margin" style="left: 1031px; visibility: visible;"></div></div><div class="ace_layer ace_marker-layer"><div style="height: 26px; top: 104px; left: 0px; right: 0px;" class="ace_active-line"></div></div><div class="ace_layer ace_text-layer" style="height: 1000000px; margin: 0px 4px; transform: translate(0px, -52px);"><div style="height: 26px; top: 52px;" class="ace_line"><span class="ace_keyword">#include</span><span class="ace_constant ace_other">&lt;math.h&gt;</span></div><div style="height: 26px; top: 78px;" class="ace_line"></div><div style="height: 26px; top: 104px;" class="ace_line"></div><div style="height: 26px; top: 130px;" class="ace_line"><span class="ace_keyword">#define</span><span class="ace_constant ace_other"> f(x) (x*exp(x)-cos(x))</span></div><div style="height: 26px; top: 156px;" class="ace_line"></div><div style="height: 26px; top: 182px;" class="ace_line"> <span class="ace_storage ace_type">int</span> <span class="ace_identifier">main</span><span class="ace_paren ace_lparen">(</span><span class="ace_paren ace_rparen">)</span></div><div style="height: 26px; top: 208px;" class="ace_line"> <span class="ace_paren ace_lparen">{</span></div><div style="height: 26px; top: 234px;" class="ace_line">    <span class="ace_storage ace_type">float</span> <span class="ace_identifier">a</span><span class="ace_punctuation ace_operator">,</span><span class="ace_identifier">b</span><span class="ace_punctuation ace_operator">,</span><span class="ace_identifier">c</span><span class="ace_punctuation ace_operator">;</span></div></div><div class="ace_layer ace_marker-layer"></div><div class="ace_layer ace_cursor-layer ace_hidden-cursors"><div class="ace_cursor" style="display: block; transform: translate(4px, 104px); width: 13px; height: 26px;"></div></div></div></div><div class="ace_scrollbar ace_scrollbar-v" style="width: 17px; bottom: 12px;"><div class="ace_scrollbar-inner" style="width: 17px; height: 936px;">&nbsp;</div></div><div class="ace_scrollbar ace_scrollbar-h" style="height: 17px; left: 58.6641px; right: 12px;"><div class="ace_scrollbar-inner" style="height: 17px; width: 1086px;">&nbsp;</div></div><div style="height: auto; width: auto; top: 0px; left: 0px; visibility: hidden; position: absolute; white-space: pre; font: inherit; overflow: hidden;"><div style="height: auto; width: auto; top: 0px; left: 0px; visibility: hidden; position: absolute; white-space: pre; font: inherit; overflow: visible;">הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה</div><div style="height: auto; width: auto; top: 0px; left: 0px; visibility: hidden; position: absolute; white-space: pre; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; font-size-adjust: inherit; font-kerning: inherit; font-optical-sizing: inherit; font-language-override: inherit; font-feature-settings: inherit; font-variation-settings: inherit; overflow: visible;">XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX</div></div></div>
//   </div>
//   </div>

//     <!-- For Edit code footer-->
//     <div class="m-2 d-flex" style="color: white; ">
//       <div style="width: 6vw;cursor: pointer;background-color: green" class="fw-bold fst-italic branch_footer rounded text-center">
//         main
//       </div>
//       <div style="width: 6vw;cursor: pointer;background-color: #282C34;" class="fw-bold rounded text-center ms-2" onclick="editCode('1')">
//         edit
//       </div>
//     </div>
  
//   </div>