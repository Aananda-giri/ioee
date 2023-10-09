import math
from .models import Code, Branch, Photo, Codes
from .forms import CodeForm
from django.shortcuts import render, get_object_or_404
from django.core.mail import BadHeaderError #, send_mail
from django.urls import reverse


from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect, JsonResponse
from .forms import EmailForm
from django.conf import settings
from django.core import serializers
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch

import requests, os
from requests.structures import CaseInsensitiveDict
from .functions import DriveFunctions
from .serializers import ContainerSerializer
from django.db.models import Prefetch
from django.utils import timezone

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





# ----------------------------------
# File upload to Google Drive
# ----------------------------------
from django.shortcuts import render, redirect
from django.conf import settings
from googleapiclient.discovery import build
from google.oauth2 import service_account
from .forms import UploadFileForm
# from .models import File

def save_file(files, author=None, title=None, description=None):
    print(f'\n---------- file info ----------\n')
    for file in files:
        print(file.name)
        # save file to media folder
        if not os.path.exists('uploads/file_upload'):
            if not os.path.exists('uploads'):
                os.mkdir('uploads')
            os.mkdir('uploads/file_upload')
        with open(f'uploads/file_upload/{file.name}', 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
    print(f'\n author: {author}, title: {title}, description:{description}')


# --------------------
# for testing purpose
# --------------------
def upload_files(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid() or True:
            files = request.FILES.getlist('file_field')
            print('files', files,'\n\n')
            author = form.cleaned_data.get('title')
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            print(f'request.Files:{request.FILES}')
            save_file(files, author, title, description)
            
            # upload files to google drive
            # drive_links = DriveFunctions.upload_multiple_files(files)
            # print(drive_links)

            # save to django models
            # File.objects.create(author='anon', title='some title', description='desc',  drive_links=drive_links)
            

            return redirect('success')  # Redirect to success page
    else:
        form = UploadFileForm()
    
    containers = Container.objects.prefetch_related('files', 'codes')
    serializer = ContainerSerializer(containers, many=True)
    context = {
        'container_form': ContainerForm(),
        'file_form': FilesForm(),
        'code_form': CodesForm(),
        'form': form,
        'containers':serializer.data
    }
    
    return render(request, 'code_share/upload_files.html', context)

# ------------------
# New views Format
# ------------------
from django.shortcuts import render, redirect
from .forms import ContainerForm, FilesForm, CodesForm
from .models import Container

def filter_containers(filter=True):
    
    '''
     * removes spam code
     * and remove empty containers created more than 1 day ago
    '''

    
    if filter == True:
        # Create a Prefetch object to filter out spam codes
        non_spam_codes_prefetch = Prefetch('codes', queryset=Codes.objects.filter(is_spam=False), to_attr='non_spam_codes')

        # Filter out containers created more than 1 day ago and have non-spam codes or no files
        one_day_ago = timezone.now() - timezone.timedelta(days=1)

        # Fetch containers with non-spam codes using the Prefetch
        containers_with_non_spam_codes = Container.objects.order_by('-created_on').prefetch_related(
            non_spam_codes_prefetch,
            'files'
        )#.filter(created_on__lte=one_day_ago)


        filtered_containers = [
            container for container in containers_with_non_spam_codes
            # display if: "Not private code and"
            # 1. created less than 1 day ago
            # 2. has non-spam codes
            # 3. has files
            if (container.is_private == False) and (one_day_ago <= container.created_on) or (container.non_spam_codes) or (container.files.all())
            # if container.non_spam_codes and not container.files.all()
        ][:25]

        return filtered_containers
    else:
        # containers = Container.objects.order_by('-created_on').prefetch_related('files', 'codes')[:25]
        
        containers = Container.objects.order_by('-created_on').prefetch_related(
            Prefetch('codes', queryset=Codes.objects.filter(is_spam=False)),
            'files'
            )[:25]
        return containers


def create_container(request, page=1, is_new_container='False'):
    container_form = ContainerForm()
    file_form = FilesForm()
    code_form = CodesForm()

    if request.method == 'POST':
            container_form = ContainerForm(request.POST)
            file_form = FilesForm(request.POST)
            code_form = CodesForm(request.POST)

            # if container_form.is_valid() and file_form.is_valid() and code_form.is_valid():
            body = request.POST.get("body", None)
            files = request.FILES.getlist('file_field')
            if (body == None or body.strip() == '') and files == []:
                return render(request, 'code_share/home2.html', {'container_form': container_form, 'file_form': file_form, 'code_form': code_form, 'message':"Body and Files can't be empty"})
            
            if body != None and body.strip() != '':
                code_data = [
                    {'body': body}
                ]
            else:
                code_data = None
            title = request.POST.get("title", None)
            author = request.POST.get("author", None)
            email = request.POST.get("email", None)
            tags = request.POST.get("tags", None).split(' ')
            
            is_private = request.POST.get("is_private", None)
            is_private = (False, True) [is_private=="on"]       #To hide the private code

            # print all fields send by requests
            print(f'{request.POST}')
            container_data = {
                'title': title if (title != None) else '',
                'author': author if (author != None) else '',
                # 'created_on': '2023-07-08',
                # 'unique_uuid': '123e4567-e89b-12d3-a456-426614174000',
                'tags': tags if (tags != None) else [],
                # 'likes_count': 10
            }

            
            # get_info(files, author, title, description)
            if len(files) > 0:
                save_file(files, author, title, body)
                # upload files to google drive
                uploaded_file_data = DriveFunctions.upload_multiple_files(files)
            else:
                uploaded_file_data = None
            
            print(f'\n\n title:{title}, \nauthor:{author}, \nemail:{email}, \ntags:{tags}, \nis_private:{is_private}, \nbody:{body}, \nfiles:{files}')
            
            Container.create_container_file_code(container_data=container_data, file_data=uploaded_file_data, code_data=code_data)
            # container_data = container_form.cleaned_data
            # file_data = [file_form.cleaned_data]
            # code_data = [code_form.cleaned_data]
            # print(f'container_data:{container_data}, file_data:{file_data}, code_data:{code_data}')
            # container = Container.create_container_file_code(
            #     container_data=container_data,
            #     file_data=file_data,
            #     code_data=code_data
            # )
            # return redirect('success')#, container_id=container.unique_uuid)
        
    context = {
        'container_form': container_form,
        'file_form': file_form,
        'code_form': code_form
    }
    

    containers = filter_containers(filter=True)
    serializer = ContainerSerializer(containers, many=True)
    is_new_container = True if is_new_container=='True' else False
    is_new_container = True if (containers[0].files.all().count() == 0 and containers[0].codes.all().count() == 0) else is_new_container
    print(f'is_new_container:\'{is_new_container}\', {type(is_new_container)}')
    return render(request, 'code_share/home2.html', {'containers':serializer.data, 'context':context, 'is_new_container':is_new_container})
    return JsonResponse(serializer.data, safe=False)

    message = None
    max_pages = math.ceil(Container.objects.all().count()/10)
    containers = Container.objects.filter(is_private=False).order_by('-created_on')[(page-1)*10:(page)*10]
    return render(request, 'code_share/home2.html', {'context':context, 'containers':containers})
    data = serializers.serialize('json', containers)
    files = Files.objects.filter(is_private=False).order_by('-created_on')
    branches = serializers.serialize('json', branches)
    images = Photo.objects.all()
    #data = serializers.serialize('json', {'codes': codes, 'new_code': new_code, 'code_form': code_form} )

    return render(request, 'code_share/home.html', {'data': data, 'codes': new_code, 'code_form': code_form, 'branches':branches, 'search_term':'', 'max_pages' : max_pages, 'message': message})


'''
message: new code/file
Add Code -> new_Container
'''
# ---------------------
# ------- create new container -------
# ---------------------
def new_container(request):
    print('\n\n redirecting')
    # return redirect('create_container')
    if request.method == 'POST':
        title = request.POST.get("title", None)
        author = request.POST.get("author", None)
        email = request.POST.get("email", None)
        tags = request.POST.get("tags", None).split(' ')
        
        is_private = request.POST.get("is_private", None)
        is_private = (False, True) [is_private=="on"]       #To hide the private code
        author_ip = author_ip = get_client_ip(request)

        # print all fields send by requests
        
        container_data = {
            'title': title if (title != None) else '',
            'author': author if (author != None) else '',
            # 'created_on': '2023-07-08',
            # 'unique_uuid': '123e4567-e89b-12d3-a456-426614174000',
            'tags': tags if (tags != None) else [],
            'author_email': email,
            'is_private': is_private,
            'author_ip': author_ip,
            # 'likes_count': 10
        }

        print(f'container_data:{container_data} \n\n  request.POST: {request.POST}')
        container = Container.objects.create(**container_data)
        
        # return JsonResponse({'container_uuid': container.unique_uuid})
        # redirect to create_container
        return redirect(reverse('home2', kwargs={'page':1, 'is_new_container':'True'}))
    else:
        return JsonResponse({'error': 'Container creation failed.'}, status=400)

def upload_success(request):
    return render(request, 'code_share/upload_success.html')

def container_list(request):
    containers = Container.objects.all()
    serializer = ContainerSerializer(containers, many=True)
    return JsonResponse(serializer.data, safe=False)

def editor(request):
    return render(request, 'code_share/editor.html')




import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# ---------------------
# ------- Test -------
# ---------------------
@csrf_exempt
def upload_multiple_files(request):
    print(f'methid: {request.method}')
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        container_uuid = request.POST.get('container_uuid')
        
        print(f'container_uuid: \'{container_uuid}\'')
        if len(files) == 0:
            print(f'length of files is zero')
            return JsonResponse({'error': 'No files found'}, status=400)
        # for file in files:
        #     # Save each file to the /uploads directory using Django's default storage
        #     file_path = os.path.join(settings.MEDIA_ROOT, 'uploads/file_upload', file.name)
        #     default_storage.save(file_path, file)

        #     # Get the URL of the uploaded file
        #     file_url = default_storage.url(file_path)
        #     file_urls.append(file_url)
        # save files to directory
        print(files)
        save_file(files)
        print('saved')

        # upload files to google drive
        file_data = DriveFunctions.upload_multiple_files(files)    # returns list of urls
        print(f'file_data: {file_data}')
        
        # # save file url to database
        file_metadata = Container.bulk_create_files(container_uuid, file_data)
        # files_to_create = [Files(container=container, filename='1',type='img', link= file_data) for file_data in file_data_list]
        # Container.create_container_file_code(container_data=container_data, file_data=uploaded_file_data, code_data=code_data)

        return JsonResponse({'metadata': file_metadata}, status=200)
    # return render(request, 'code_share/upload_multiple.html')
    return JsonResponse({'error': 'File upload failed.'}, status=400)

'''
upload code
backend-frondend integration
'''
# ---------------------
# ------- Test -------
# ---------------------
def upload_one_code(request):
    if request.method == 'POST':
        container_id = request.POST.get("container_uuid", None)
        code =  request.POST.get("code", None)
        print(code)
        filename =  request.POST.get("filename", 'code')
        
        print(f'0code:{code}, container_id: {container_id}, filename:{filename}')
        if code !=None and code.strip() != '' and container_id != None and container_id.strip() != '':
            print(f'code:{code}, container_id: {container_id}, filename:{filename}')
            # save code
            saved_data = Container.add_one_code(container_id, filename, code)
            
            print(f'saved code successfully! returning metadata:{saved_data}')
            return JsonResponse({'metadata': saved_data}, status=200)
        else:
            return JsonResponse({'error': 'Code upload failed.'}, status=400)

'''
bulk create files
bulk create codes
post file, code
'''