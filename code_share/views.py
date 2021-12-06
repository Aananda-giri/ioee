from .models import Code
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail

from django.shortcuts import render
from .forms import EmailForm
from django.conf import settings


#source: https://djangocentral.com/creating-comments-system-with-django/
def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()


    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})

def format_email_message_body(uuid):
    message = "Here is your code: https://ioee.herokuapp.com/code/{}/\n\n".format(str(uuid))
    #message += "anyone who has this link has right to delete it?"
    #message += "You can delete this code by verifying this email"
    return(message)

def toy_post(request):
    template_name = 'post_detail.html'
    #post = get_object_or_404(Post, slug=slug)
    comments = Code.objects.using('fuse_attend').all()
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = request.POST.get("body", None);
            author = request.POST.get("name", None);
            email = request.POST.get("email", None);
            print(comment, author, email)
            # Create Comment object but don't save to database yet
            new_comment = Code.objects.using('fuse_attend').create(comment=comment, author=author, email=email)
            # Assign the current post to the comment
            #new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            print('\n\n {} \n\n'.format(str(new_comment.id)))
            if email.strip()!='':
                send_mail_please(recipient= [email], subject="code", message=format_email_message_body(str(new_comment.id)))
    else:
        comment_form = CommentForm()
    return render(request, 'code_share/template.html', {'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})

'''
def Code(request):
    if request.is_ajax and request.method == "POST":
        # get the nick name from the client side.
        #post = request.POST.get("username", None);
        comment = request.POST.get("comment", None);
        author = request.POST.get("author", None);
        
    if not str(comment).strip()=='':
        Codes.objects.using('fuse_attend').create(comment=str(comment), author = str(author))
        return HttpResponse('Successfully commented')
    
    else:
        return HttpResponse('Comment is empty')

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