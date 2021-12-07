from .models import Code
from .forms import CodeForm
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail

from django.shortcuts import render
from .forms import EmailForm
from django.conf import settings


#source: https://djangocentral.com/creating-codes-system-with-django/
def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    codes = post.codes.filter(active=True)
    new_code = None
    # code posted
    if request.method == 'POST':
        code_form = CodeForm(data=request.POST)
        if code_form.is_valid():

            # Create code object but don't save to database yet
            new_code = code_form.save(commit=False)
            # Assign the current post to the code
            new_code.post = post
            # Save the code to the database
            new_code.save()
    else:
        code_form = CodeForm()


    return render(request, template_name, {'post': post,
                                           'codes': codes,
                                           'new_code': new_code,
                                           'code_form': code_form})

def format_email_message_body(uuid):
    message = "Here is your code: https://ioee.herokuapp.com/code/{}/\n\n".format(str(uuid))
    #message += "anyone who has this link has right to delete it?"
    #message += "You can delete this code by verifying this email"
    return(message)

def home(request):
    template_name = 'post_detail.html'
    #post = get_object_or_404(Post, slug=slug)
    codes = Code.objects.using('fuse_attend').all().order_by('-created_on')
    new_code = None
    # code posted
    if request.method == 'POST':
        code_form = CodeForm(data=request.POST)
        if code_form.is_valid():
            code = request.POST.get("code", None)
            title = request.POST.get("title", None)
            author = request.POST.get("author", None)
            email = request.POST.get("email", None)
            tags = request.POST.get("tags", None).split(' ')
            print(code, title, email)
            # Create code object but don't save to database yet
            new_code = Code.objects.using('fuse_attend').create(code=code, email=email, title=title, tags=tags, author=author)
            # Assign the current post to the code
            #new_code.post = post
            # Save the code to the database
            new_code.save()
            print('\n\n {} \n\n'.format(str(new_code.id)))
            if email.strip()!='':
                send_mail_please(recipient= [email], subject="code", message=format_email_message_body(str(new_code.id)))
    else:
        code_form = CodeForm()
    return render(request, 'code_share/home.html', {'codes': codes, 'new_code': new_code, 'code_form': code_form})

'''
def Code(request):
    if request.is_ajax and request.method == "POST":
        # get the nick name from the client side.
        #post = request.POST.get("username", None);
        code = request.POST.get("code", None);
        author = request.POST.get("author", None);
        
    if not str(code).strip()=='':
        Codes.objects.using('fuse_attend').create(code=str(code), author = str(author))
        return HttpResponse('Successfully codeed')
    
    else:
        return HttpResponse('code is empty')

'''


def sendMail(request):

    # create a variable to keep track of the form
    messageSent = False

    # check if form has been submitted
    if request.method == 'POST':

        form = EmailForm(request.POST)

        # check if data from the form is clean
        if form.is_valid():
            cd = form.cleaned_data
            subject = "Sending an email with Django"
            message = cd['message']

            # send the email to the recipent
            send_mail(subject, message,
                      settings.DEFAULT_FROM_EMAIL, [cd['recipient']])

            # set the variable initially created to True
            messageSent = True

    else:
        form = EmailForm()

    return render(request, 'code_share/mail.html', {

        'form': form,
        'messageSent': messageSent,

    })

def send_mail_please(recipient, subject="uuid", message='hello World'):
            # create a variable to keep track of the form
            #messageSent = False
            #recipient = 'aanandaprashadgiri@gmail.com'
            #subject = "Sending an email with Django"
            #message = cd['message']

            # send the email to the recipent
            send_mail(subject, message,
                      settings.DEFAULT_FROM_EMAIL, recipient)

            # set the variable initially created to True
            messageSent = True

def code_by_uuid(request, uuid):
    code = Code.objects.using('fuse_attend').get(id=uuid)
    return render(request, 'code_share/individual_code.html', {'code':code})