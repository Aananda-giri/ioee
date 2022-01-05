from .models import Code, Branch
from .forms import CodeForm
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail

from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from .forms import EmailForm
from django.conf import settings
from django.core import serializers
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.auth.decorators import login_required

#@login_required
def home(request):
    print('\n In home \n')
    template_name = 'code_share/home.html'
    #post = get_object_or_404(Post, slug=slug)

    new_code = None
    # code posted
    if request.method == 'POST' and request.is_ajax:
            code = request.POST.get("code", None)
            code = code[1:-1] # front_end sending code with quotes before and after the code
            #code_form = CodeForm(data=request.GET)
            #if code_form.is_valid():
            # code = request.GET.get("code", None)
            title = request.POST.get("title", None)
            author = request.POST.get("author", None)
            email = request.POST.get("email", None)
            tags = request.POST.get("tags", None).split(' ')
            
            private_code = request.POST.get("private_code", None)
            print('\n\nprivate_code:\'{}\' Type:{}'.format(private_code, type(private_code)))
            private_code = (False, True) [private_code=="true"]       #To hide the private code

            print(private_code)
            print(code, title, email)
            # Create code object but don't save to database yet
            new_code = Code.objects.using('fuse_attend').create(
                code=code, email=email, title=title, tags=tags, author=author, stars=0, private_code=private_code)
            # Assign the current post to the code
            #new_code.post = post
            # Save the code to the database
            new_code.save()
            print('\n\n {} \n\n'.format(str(new_code.id)))
            if email.strip() != '':
                send_mail_please(recipient=[
                                 email], subject="code", message=format_email_message_body(str(new_code.id)))
            return HttpResponse('reload')
    # else:
    code_form = CodeForm()
    codes = Code.objects.using('fuse_attend').filter(private_code=False).order_by('-created_on')
    data = serializers.serialize('json', codes)
    branches = Branch.objects.using('fuse_attend').filter(private_code=False).order_by('-created_on')
    branches = serializers.serialize('json', branches)
    #data = serializers.serialize('json', {'codes': codes, 'new_code': new_code, 'code_form': code_form} )

    return render(request, 'code_share/home.html', {'data': data, 'new_code': new_code, 'code_form': code_form, 'branches':branches, 'search_term':''})


def format_email_message_body(uuid):
    message = "Here is your code: https://ioee.herokuapp.com/code/{}/\n\n".format(
        str(uuid))
    #message += "anyone who has this link has right to delete it?"
    #message += "You can delete this code by verifying this email"
    return(message)


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
    # return render(request, 'code_share/individual_code.html', {'code':code})
    code_form = CodeForm()
    #codes = Code.objects.using('fuse_attend').all().order_by('-created_on')
    data = serializers.serialize('json', [code])
    #data = serializers.serialize('json', {'codes': codes, 'new_code': new_code, 'code_form': code_form} )

    return render(request, 'code_share/home.html', {'data': data, 'code_form': code_form, 'branches':[]})

def edit_code(request, parent_id=None):
    print('\n\n inside edit code \n\n')
    
    if request.method == 'POST' and request.is_ajax:
        code = request.POST.get("code", None)
        code = code[1:-1] # front_end sending code with quotes before and after the code
        parent_id = request.POST.get("parent_id", None)
        print(code, parent_id)
        # Create code object but don't save to database yet
        original_code = Code.objects.using('fuse_attend').get(id=parent_id)
        branch = Branch.objects.using('fuse_attend').create(
            Parent=original_code, code=code, email=original_code.email, title=original_code.title, tags=original_code.tags, author=original_code.author, private_code=original_code.private_code)
        branch.save()  # Saves the branch
        # new_code = Code.objects.using('fuse_attend').create(
        # code=code, email=email, title=title, tags=tags, author=author)
        # Assign the current post to the code

        print('\n\n {} \n\n'.format(str(branch.id)))
        if email.strip() != '':
            send_mail_please(recipient=[
                             email], subject="code", message=format_email_message_body(str(new_code.id)))

        #codes = Code.objects.using('fuse_attend').all().order_by('-created_on')
        #data = serializers.serialize('json', codes)
        #data = serializers.serialize('json', {'codes': codes, 'new_code': new_code, 'code_form': code_form} )
        parent_data = None
        # return render(request, template_name, {'data': data, 'new_code': new_code, 'code_form': code_form})
    else:
        parent_data = Code.objects.using('fuse_attend').get(id=parent_id)
        code_form = CodeForm()
        #codes = Code.objects.using('fuse_attend').all().order_by('-created_on')
        #parent_data = serializers.serialize('json', code)
        branch = None
        #data = serializers.serialize('json', {'codes': codes, 'new_code': new_code, 'code_form': code_form} )

    code_form = CodeForm()
    HttpResponseRedirect(home)

# def edit_code(request, parent_id=None):
#     template_name = 'code_share/edit.html'
#     print('\n\n inside edit code \n\n')
#     #post = get_object_or_404(Post, slug=slug)

#     new_code = None
#     # # code posted
#     if request.method == 'POST' and parent_id == None:
#          data = request.POST.get("data", None)
#          print(data)
    #     #code_form = CodeForm(data=request.POST)
    #     # if code_form.is_valid():
    #     #id = request.POST.get("id", None)
    #     parent_id = request.POST.get("parent_id", None)
    #     code = request.POST.get("code", None)
    #     title = request.POST.get("title", None)
    #     author = request.POST.get("author", None)
    #     email = request.POST.get("email", None)
    #     tags = request.POST.get("tags", None).split(' ')
    #     print(code, title, email)
    #     # Create code object but don't save to database yet
    #     #code = Code.objects.using('fuse_attend').get(id=parent_id)
    #     branch = Branch.objects.using('fuse_attend').create(
    #         originalCode=code, code=code, email=email, title=title, tags=tags, author=author)
    #     branch.save()  # Saves the branch
    #     # new_code = Code.objects.using('fuse_attend').create(
    #     # code=code, email=email, title=title, tags=tags, author=author)
    #     # Assign the current post to the code

    #     print('\n\n {} \n\n'.format(str(new_code.id)))
    #     if email.strip() != '':
    #         send_mail_please(recipient=[
    #                          email], subject="code", message=format_email_message_body(str(new_code.id)))

    #     #codes = Code.objects.using('fuse_attend').all().order_by('-created_on')
    #     #data = serializers.serialize('json', codes)
    #     #data = serializers.serialize('json', {'codes': codes, 'new_code': new_code, 'code_form': code_form} )
    #     parent_data = None
    #     # return render(request, template_name, {'data': data, 'new_code': new_code, 'code_form': code_form})
    # else:
    #     parent_data = Code.objects.using('fuse_attend').get(id=parent_id)
    #     code_form = CodeForm()
    #     #codes = Code.objects.using('fuse_attend').all().order_by('-created_on')
    #     #parent_data = serializers.serialize('json', code)
    #     branch = None
    #     #data = serializers.serialize('json', {'codes': codes, 'new_code': new_code, 'code_form': code_form} )

    # code_form = CodeForm()
    # return render(request, template_name, {'parent_data': parent_data, 'branch': branch, 'code_form': code_form, 'parent_id': parent_id})

###########################################
# Unused views
###########################################

# source: https://djangocentral.com/creating-codes-system-with-django/


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


def ssl_cert(request):
    # requires heroku hobby dynos
    return HttpResponse('3ufveaLc9JnIgj9y5-f9jrhb8Vgz2fSAFTbKguBTMYk.s1y7_YhjSk90w1NT8OBQ3LfEfRjn-eWv8R014Xl2Cco')


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


def add_star(request):
    if request.is_ajax and request.method == "POST":
        # get the nick name from the client side.
        parent_id = request.POST.get("parent_id", None)

        unique_ip = request.POST.get("unique_ip", None)
        print('\nparent_id:{}, unique_ip:{}\n'.format(parent_id, unique_ip))
        # implement one computer one vote

        code = Code.objects.using('fuse_attend').get(id=parent_id)
        code.stars += 1
        code.save()
    else:
        print('fucking else')
    return HttpResponse('Done')

def search_code(request):
    if request.method == "GET":
        # get the nick name from the client side.
        search_term = request.GET.get("search_query", None)
        print(search_term)
        codes_list = Code.objects.using('fuse_attend').annotate(
        search=SearchVector('title','author','email','tags', 'code')).filter(search=search_term)
        
        codes=[]
        for code in codes_list:
            codes.append(code)
        codes = serializers.serialize('json', codes, )
        print(codes)
        #print('peoples_list:\n\n'+str(peoples_list))
    else:
        print('\nfucking request not get\n')
    return render(request, 'code_share/home.html', {'data': codes, 'new_code': [], 'code_form': CodeForm(), 'branches':[], 'search_term':search_term})
    #  {'people':people}, status = 200)

@login_required()
def delete_code(request, parent_id=None):
    # return render(request, 'code_share/home.html', {})
    print('\n\n inside delete code \n\n')
    
    if request.method == 'POST' and request.is_ajax:
        code_id = request.POST.get("code_id", None)
        if request.user.is_authenticated:
            print('user logged in')
            print(request.user.email)
        
        code = Code.objects.using('fuse_attend').get(id=code_id)
        print(code_id)
        print(code.email)
        if code.email == request.user.email:
            code.delete()
            # return render(request, template_name, {'data': data, 'new_code': new_code, 'code_form': code_form})
            response = "Succesfully deleted!!! \n please reload to view the effect"
        else:
            response = "your email doesn't match with author\'s email address.....\n Only author can delete the code"
        # print("\n\n not request.method == 'POST' and request.is_ajax \n\n")
    #return HttpResponse(response)
    return HttpResponseRedirect(home)
