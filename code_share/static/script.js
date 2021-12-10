const codecs = [
  {
    id: "1",
    author: "Ritik",
    title: "Circular Queue",
    timestamp: "Dec. 8, 2021, 10:34 a.m.",
    code: `#include<stdio.h>
      #include<stdlib.h>
      #define size 4
      
      void push();
      void pop();
      void show();
      int rear=-1, front=-1,inp_array[size];
      int main(){
      int choice;
      while(1){
      printf("operations performed by queue\n");
      printf("\n1.push\n2.pop\n3.show\n4.end\n\n");
      scanf("%d", &choice);
      switch(choice){
      case 1:
      push();
      break;
      case 2:
      pop();
      break;
      case 3:
      show();
      break;
      case 4:exit(0);
      default:printf("Invalid Choice\n");
      
      }
      }
      
      }
      void push(){
      int x,i;
      if((rear==size-1&& front==0)||(front==rear+1)){
      printf("\nOverflow\n");
      }
      else if(front==-1){
      front=0;
      rear=0;
      }
      
      else{
      printf("print the element to be inserted\n");
      scanf("%d",&x);
      rear=(rear+1)%size;
      printf("rear:%d\t",rear);
      printf("front:%d",front);
      inp_array[rear]=x;
      
      }
      }
      
      void pop(){
      if(front==-1){
      printf("\nUnderflow");
      }else if(front==rear){
      front=-1;
      rear=-1;}
      else{
      
      printf("\npopped element=%d\n",inp_array[front]);
      front=(front+1)%size;
      printf("rear:%d\t",rear);
      printf("front:%d\n",front);
      }
      }
      
      void show(){
      int i;
      if(front==-1){
      printf("\nUnderflow!!");
      }else{
      printf("\nElements present in the stack:\n");
      if(front>rear){
      
      for(i=0;i<=(size-1);i++){
      printf("show:%d\n",inp_array[i]);
      
      }}
      else{
      for(i=front;i<=(rear);i++){
      printf("show:%d\n",inp_array[i]);
      
      }
      }
      }
      }`,
  },
  {
    id: "2",
    author: "Ritik",
    title: "Secant Method",
    timestamp: "Dec. 8, 2021, 10:33 a.m.",
    code: `#include<stdio.h>
      #include<conio.h>
      #include<math.h>
      #define f(x) (x*x*x-2*x-5)
      int main(){
      float x0,x1,x2;
      int i=0;
      printf("Enter ther value of x0 and x1:\n");
      scanf("%f%f",&x0,&x1);
      printf("No.ofsteps\tx0\tx1\tx2\tf(x1)\tf(x2)\tf(x0)\n");
      printf("%d\t\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\n",i+1,x0,x1,x2,f(x1),f(x2),f(x0));
      do{
      
      x2=(f(x1)*x0-f(x0)*x1)/(f(x1)-f(x0));
      x0=x1;
      x1=x2;
      printf("%d\t\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\n",i+1,x0,x1,x2,f(x1),f(x2),f(x0));
      i++;
      
      }while(fabs(x1-x0)>0.00001);
      printf("Required root=%f",x2);
      printf("\n f(x2)=%f",f(x2));
      
      }
      
      
      `,
  },
  {
    id: "3",
    author: "katrina",
    title: "Newton Raphson",
    timestamp: "Dec. 7, 2021, 10:13 a.m.",
    code: `#include<stdio.h>
        #include<stdlib.h>
        #define size 4
        
        void push();
        void pop();
        void show();
        int rear=-1, front=0,inp_array[size];
        int main(){
        int choice;
        while(1){
        printf("operations performed by queue");
        printf("\n1.push\n2.pop\n3.show\n4.end\n\n");
        scanf("%d", &choice);
        switch(choice){
        case 1:
        push();
        break;
        case 2:
        pop();
        break;
        case 3:
        show();
        break;
        case 4:exit(0);
        default:printf("Invalid Choice");
        
        }
        }
        
        }
        void push(){
        int x,i;
        if(rear==size-1){
        printf("\n Overflow");
        }
        else{
        printf("print the element to be inserted");
        scanf("%d",&x);
        rear=rear+1;
        inp_array[rear]=x;
        
        
        }
        }
        
        void pop(){
        if(front==-1||front>rear){
        printf("\n Overflow");
        }else{
        printf("\npopped element=%d",inp_array[front]);
        front++;
        }
        }
        
        void show(){
        int i;
        if(front==-1||front>rear){
        printf("\nUnderflow!!");
        }else{
        printf("\n Elements present in the stack:\n ");
        for(i=front;i<=rear;i++){
        printf("show:%d\n",inp_array[i]);
        
        }
        }
        }
      
      `,
  },
];

function createEditor(key, i) {
  //for (key in codes) {
  let accordion = document.getElementById("accordionExample");
  accordion.innerHTML += `<div class="accordion-item my-3">
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
  >
  <div class="accordion-body editor">
    <div class='editor__code 'id="editor${i}"></div>
  </div>
  </div>
  </div>`;
  //}
}

// function setupEditor(codes) {
//   for (i = 0; i < 10; i++) {
//     window.editor = ace.edit(`editor${key["id"]}`);
//     editor.setTheme("ace/theme/one_dark");
//     editor.getSession().setMode("ace/mode/c_cpp");
//     editor.setValue(key.code, 1); //1 = moves cursor to end

//     editor.setReadOnly(true);
//     editor.setOptions({
//       fontSize: "16pt",
//       showLineNumbers: true,
//       showGutter: true,
//       // vScrollBarAlwaysVisible: true,
//     });
//   }
// }

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
