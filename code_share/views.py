import math
from .models import Code, Branch, Photo
from .forms import CodeForm
from django.shortcuts import render, get_object_or_404
from django.core.mail import BadHeaderError #, send_mail


from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from .forms import EmailForm
from django.conf import settings
from django.core import serializers
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.auth.decorators import login_required

import requests, os
from requests.structures import CaseInsensitiveDict

#source: https://stackoverflow.com/questions/18264304/get-clients-real-ip-address-on-heroku#answer-18517550
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@login_required(login_url='login')
def addPhoto(request):
    user = request.user

    categories = user.category_set.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                user=user,
                name=data['category_new'])
        else:
            category = None

        for image in images:
            photo = Photo.objects.create(
                category=category,
                description=data['description'],
                image=image,
            )

        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'photos/add.html', context)

#@login_required
def home(request):
    #print('\n\nIp: ' + str(get_client_ip(request)) +'\n\n')
    template_name = 'code_share/home.html'
    #post = get_object_or_404(Post, slug=slug)

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
            
            private_code = request.POST.get("private_code", None)
            private_code = (False, True) [private_code=="on"]       #To hide the private code
            
            
            print(private_code)
            print(code, title, email)
            # Create code object but don't save to database yet
            new_code = Code.objects.create(
                code=code, email=email, title=title, tags=tags, author=author, stars=0, private_code=private_code, author_ip = get_client_ip(request))
            # Assign the current post to the code
            #new_code.post = post
            # Save the code to the database
            new_code.save()
            
            # Saving images if given
            images = request.FILES.getlist('images')
            for image in images:
                photo = Photo.objects.create(
                    #category = category,
                    title = title,
                    image=image,
                    parent_code = new_code
            )
            
            print('\n\n {} \n\n'.format(str(new_code.id)))
            if email.strip() != '':
                sent = send_mail_please(recipient=[
                                 email], subject="code", message=format_email_message_body(str(new_code.id)))
                if sent:
                    # valid email true
                    new_code.valid_email=True
                    new_code.save()
    # else:
    code_form = CodeForm()
    codes = Code.objects.filter(private_code=False).order_by('-created_on')
    data = serializers.serialize('json', codes)
    branches = Branch.objects.filter(private_code=False).order_by('-created_on')
    branches = serializers.serialize('json', branches)
    images = Photo.objects.all()
    #data = serializers.serialize('json', {'codes': codes, 'new_code': new_code, 'code_form': code_form} )

    return render(request, 'code_share/home.html', {'data': data, codes: new_code, 'code_form': code_form, 'branches':branches, 'search_term':''})

def search_code(request):
    if request.method == "GET":
        # get the nick name from the client side.
        search_term = request.GET.get("search_query", None)
        print(search_term)
        codes_list = Code.objects.annotate(
        search=SearchVector('title','author','email','tags', 'code')).filter(search=search_term)
        
        codes=[]
        for code in codes_list:
            codes.append(code)
        codes = serializers.serialize('json', codes, )
        print(codes)
        #print('peoples_list:\n\n'+str(peoples_list))
        branches = Branch.objects.filter(private_code=False).order_by('-created_on')
        branches = serializers.serialize('json', branches)
    else:
        print('\nfucking request not get\n')
        branches=''
    return render(request, 'code_share/home.html', {'data': codes, 'new_code': [], 'code_form': CodeForm(), 'branches':branches, 'search_term':search_term})
    #  {'people':people}, status = 200)



#@login_required
def snippet_page(request, page=1):
    print(f"page:{page}")
    #print('\n\nIp: ' + str(get_client_ip(request)) +'\n\n')
    template_name = 'code_share/home.html'
    #post = get_object_or_404(Post, slug=slug)

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
            
            private_code = request.POST.get("private_code", None)
            private_code = (False, True) [private_code=="on"]       #To hide the private code
            
            
            print(private_code)
            print(code, title, email)
            # Create code object but don't save to database yet
            new_code = Code.objects.create(
                code=code, email=email, title=title, tags=tags, author=author, stars=0, private_code=private_code, author_ip = get_client_ip(request))
            # Assign the current post to the code
            #new_code.post = post
            
            # check if it exists in the database
            if not Code.objects.filter(code=code, email=email, title=title, tags=tags, author=author, private_code=private_code).exists():
                message = {'message':'Saved successfully', 'status':'success'}
                # Save the code to the database
                new_code.save()
            else:
                message = {'message':'Code already exists', 'status':'danger'}
            
            # Saving images if given
            images = request.FILES.getlist('images')
            for image in images:
                photo = Photo.objects.create(
                    #category = category,
                    title = title,
                    image=image,
                    parent_code = new_code
            )
            
            print('\n\n {} \n\n'.format(str(new_code.id)))
            if email.strip() != '':
                send_mail_please(recipient=[
                                 email], subject="code", message=format_email_message_body(str(new_code.id)))
    # else:
    # message = {'message':'Teest message', 'status':'success'}
    message = None
    max_pages = math.ceil(Code.objects.all().count()/10)
    code_form = CodeForm()
    codes = Code.objects.filter(private_code=False).order_by('-created_on')[(page-1)*10:(page)*10]
    data = serializers.serialize('json', codes)
    branches = Branch.objects.filter(private_code=False).order_by('-created_on')
    branches = serializers.serialize('json', branches)
    images = Photo.objects.all()
    #data = serializers.serialize('json', {'codes': codes, 'new_code': new_code, 'code_form': code_form} )

    return render(request, 'code_share/home.html', {'data': data, 'codes': new_code, 'code_form': code_form, 'branches':branches, 'search_term':'', 'max_pages' : max_pages, 'message': message})


def format_email_message_body(uuid):
    message = "Here is your code: https://ioee.herokuapp.com/code/{}/\n\n".format(
        str(uuid))
    #message += "anyone who has this link has right to delete it?"
    #message += "You can delete this code by verifying this email"
    return(message)


def send_mail_please(recipient, subject="uuid", message='hello World', name=''):
    # prevents header injection attack?
    if '\n' in recipient:
        raise BadHeaderError

    headers = CaseInsensitiveDict()
    headers["x-trustifi-key"] = os.environ.get('TRUSTIFI_KEY')
    headers["x-trustifi-secret"] = os.environ.get('TRUSTIFI_SECRET')
    headers["Content-Type"] = "application/json"

    url='https://be.trustifi.com/api/i/v1/email'
    print(f'\'{recipient}\', \'{subject}\', \'{message}\'')
    # data = """    {{
    # "recipients": [{{"email": "aanandaprashadgiri@gmail.com", "name": "aananda"}}],
    # "title": "conversation",
    # "html": "some message"
    # }}   """.format(recipient, name, subject, message)
    
    data = {
    "recipients": [{"email": recipient, "name": name}],
    "title": subject,
    "html": message}
    
    print(data)
    resp = requests.post(url, headers=headers, data=str(data))
    print(resp.text)
    return (resp.status_code==201)  # True if sent mail else False
    
    # create a variable to keep track of the form
    #messageSent = False
    #recipient = 'aanandaprashadgiri@gmail.com'
    #subject = "Sending an email with Django"
    #message = cd['message']
    
    # send the email to the recipent
    # send_mail(subject, message,
    #           settings.DEFAULT_FROM_EMAIL, recipient)
    
    # set the variable initially created to True
    # messageSent = True


def code_by_uuid(request, uuid):
    code = Code.objects.get(id=uuid)
    # return render(request, 'code_share/individual_code.html', {'code':code})
    code_form = CodeForm()
    #codes = Code.objects.all().order_by('-created_on')
    data = serializers.serialize('json', [code])
    #data = serializers.serialize('json', {'codes': codes, 'new_code': new_code, 'code_form': code_form} )

    return render(request, 'code_share/home.html', {'data': data, 'code_form': code_form, 'branches':[]})

def edit_code(request, parent_id=None):
    print('\n\n inside edit code \n\n')
    
    #request.is_ajax depreciated
    if request.method == 'POST' and request.accepts("application/json"):
        code = request.POST.get("code", None)
        code = code[1:-1].replace('\\n','\n').replace('\\r','\r') # front_end sending code with quotes before and after the code
        parent_id = request.POST.get("parent_id", None)
        print(code, parent_id)
        # Create code object but don't save to database yet
        original_code = Code.objects.get(id=parent_id)
        email = original_code.email
        
        # To pass if main_code == branch_code
        if code == original_code:
            HttpResponse('pass')

        branch = Branch.objects.create(
            Parent=original_code, code=code, email=original_code.email, title=original_code.title, tags=original_code.tags, author=original_code.author, private_code=original_code.private_code)
        branch.save()  # Saves the branch
        # new_code = Code.objects.create(
        # code=code, email=email, title=title, tags=tags, author=author)
        # Assign the current post to the code

        print('\n\n {} \n\n'.format(str(branch.id)))
        if email.strip() != '':
            send_mail_please(recipient=[
                             email], subject="code", message=format_email_message_body(str(branch.id)))

        #codes = Code.objects.all().order_by('-created_on')
        #data = serializers.serialize('json', codes)
        #data = serializers.serialize('json', {'codes': codes, 'new_code': new_code, 'code_form': code_form} )
        parent_data = None
        # return render(request, template_name, {'data': data, 'new_code': new_code, 'code_form': code_form})
    else:
        parent_data = Code.objects.get(id=parent_id)
        code_form = CodeForm()
        #codes = Code.objects.all().order_by('-created_on')
        #parent_data = serializers.serialize('json', code)
        branch = None
        #data = serializers.serialize('json', {'codes': codes, 'new_code': new_code, 'code_form': code_form} )
        print('\n\n edit_code not POST\n\n')
    code_form = CodeForm()
    return HttpResponse('reload')

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
    #     #code = Code.objects.get(id=parent_id)
    #     branch = Branch.objects.create(
    #         originalCode=code, code=code, email=email, title=title, tags=tags, author=author)
    #     branch.save()  # Saves the branch
    #     # new_code = Code.objects.create(
    #     # code=code, email=email, title=title, tags=tags, author=author)
    #     # Assign the current post to the code

    #     print('\n\n {} \n\n'.format(str(new_code.id)))
    #     if email.strip() != '':
    #         send_mail_please(recipient=[
    #                          email], subject="code", message=format_email_message_body(str(new_code.id)))

    #     #codes = Code.objects.all().order_by('-created_on')
    #     #data = serializers.serialize('json', codes)
    #     #data = serializers.serialize('json', {'codes': codes, 'new_code': new_code, 'code_form': code_form} )
    #     parent_data = None
    #     # return render(request, template_name, {'data': data, 'new_code': new_code, 'code_form': code_form})
    # else:
    #     parent_data = Code.objects.get(id=parent_id)
    #     code_form = CodeForm()
    #     #codes = Code.objects.all().order_by('-created_on')
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
        Codes.objects.create(code=str(code), author = str(author))
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

        code = Code.objects.get(id=parent_id)
        code.stars += 1
        if code.stars_ip!=None:
            if not get_client_ip(request) in code.stars_ip:
                code.stars_ip.append(get_client_ip(request))
                code.stars += 1
        else:
            code.stars_ip=[get_client_ip(request)]
            code.stars += 1
        print(code.stars_ip)
        code.save()
    else:
        print('fucking else')
    return HttpResponse('Done')

#login_required not redirecting
@login_required
def delete_code(request, parent_id=None):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(home)
    # return render(request, 'code_share/home.html', {})
    print('\n\n inside delete code \n\n')
    
    if request.method == 'GET' and request.is_ajax:
        code_id = request.GET.get("id", None)
        if request.user.is_authenticated:
            print('user logged in')
            print(request.user.email)
        
        print('\n\n' + str(code_id) + '\n\n')
        code = Code.objects.get(id=code_id)
        
        print(code.email)
        if code.email == request.user.email:
            code.delete()
            # return render(request, template_name, {'data': data, 'new_code': new_code, 'code_form': code_form})
            response = "Succesfully deleted!!! \n please reload to view the effect"
        else:
            response = "your email doesn't match with author\'s email address.....\n Only author can delete the code"
        # print("\n\n not request.method == 'POST' and request.is_ajax \n\n")
    return HttpResponseRedirect('/')
    #return HttpResponseRedirect(home)

'''def imagepage(request):
    if request.user.is_authenticated:
        if 'uploadimage' in request.POST:
            if request.method == 'POST':
 
                files  = request.FILES.getlist('uploadedfile')  
                for image in files:  
                    Images.objects.create(
                        image = image , 
                        title = request.user.name
                        
                    )
                return HttpResponseRedirect('/refresh/')
        image = Images.objects.all().order_by('-id')
        context = {
            "image" : image  ,
        }
        return render(request , "code_share/image.html" , context)
    else:
        return HttpResponseRedirect('/')'''

def refresh(request):
    return HttpResponseRedirect('/')

