#source: https://github.com/divanov11/photo-album-app

#from .models import Code, Branch, Images
#from .forms import CodeForm
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail

from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
#from .forms import EmailForm
from django.conf import settings
from django.core import serializers
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.auth.decorators import login_required


#@login_required
def ImagesHome(request):
    #print('\n\nIp: ' + str(get_client_ip(request)) +'\n\n')
    template_name = 'images/home.html'
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
            new_code = Code.objects.using('fuse_attend').create(
                code=code, email=email, title=title, tags=tags, author=author, stars=0, private_code=private_code, author_ip = get_client_ip(request))
            # Assign the current post to the code
            #new_code.post = post
            # Save the code to the database
            new_code.save()
            print('\n\n {} \n\n'.format(str(new_code.id)))
            if email.strip() != '':
                send_mail_please(recipient=[
                                 email], subject="code", message=format_email_message_body(str(new_code.id)))
    # else:
    code_form = CodeForm()
    codes = Code.objects.using('fuse_attend').filter(private_code=False).order_by('-created_on')
    data = serializers.serialize('json', codes)
    branches = Branch.objects.using('fuse_attend').filter(private_code=False).order_by('-created_on')
    branches = serializers.serialize('json', branches)
    #data = serializers.serialize('json', {'codes': codes, 'new_code': new_code, 'code_form': code_form} )

    return render(request, 'code_share/home.html', {'data': data, 'new_code': new_code, 'code_form': code_form, 'branches':branches, 'search_term':''})