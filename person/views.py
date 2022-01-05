from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import random as random

from django.template import loader

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

import mechanize
from bs4 import BeautifulSoup
import urllib
import http.cookiejar
from .models import Person
from django.views.decorators.cache import cache_page
from django.db import connections, transaction
from django.core.cache import cache # This is the memcache cache.

#from user.views import categoriesView

#780030519462
#780030523629
#OTP sent to Email: aanandaprashadgiri@gmail.com. Please enter valid OTP to submit application.
import json

from django.http import JsonResponse
from django.core import serializers


from .forms import PersonForm
from .models import Person, Photos
from django.contrib.auth.models import User
#from nepali_datetime_field.forms import NepaliDateField

# full profile pics of 076bei
def index(request):
    #people = Person.objects.using('brainmap').all()
    people = Person.objects.using('brainmap').filter(ioe_roll_no__startswith='sec076bei')
    #people = Person.objects.using('brainmap').filter(empty_profile=False)
    return render(request, 'person/home.html', {'people':[people]})

def random_person(request):
    people = [Person.objects.using('brainmap').all()[random.randint(0,35)]]
    '''stuti = Person.objects.using('brainmap').get(id=1)
    if(stuti.profile_pic == ''):
        stuti.profile_pic = get_profile_pic(stuti)
        stuti.save()
        print('pic:' + str(len(get_profile_pic(stuti))) + str(get_profile_pic(stuti)))
        print('\n\n Saved profile pic of  #',stuti.first_name)
        get_profile_pic(stuti)'''
    return render(request, 'person/index.html', {'people':[people]})


def ioe_search(request, ioe_roll_no):
    people = [Person.objects.using('brainmap').filter(ioe_roll_no=ioe_roll_no)[0]]
    return render(request, 'person/index.html', {'people':[people]})

#@cache_page(timeout=None)
def uid_search(request, uid):
    people = [Person.objects.using('brainmap').filter(id=uid)[0]]
    return render(request, 'person/index.html', {'people':[people]})

#@cache_page(timeout=None)
def search(request):
    print('\n\n search_section')
    search_term = ''
    if request.is_ajax and request.method == "GET":
        search_term = request.GET.get("search_query", None);
        
    #print('\n\n her search_term:' + str(search_term))
    #people = Person.objects.using('brainmap').all()
    
    peoples_list = Person.objects.using('brainmap').annotate(
        search=SearchVector('first_name','middle_name','last_name','tags', 'personal_details'),
        ).filter(search=search_term)
    people=[]
    for person in peoples_list:
        people.append(person)
    people = serializers.serialize('json', people, )
    #print('peoples_list:\n\n'+str(peoples_list))
    return JsonResponse({'people':people}, status = 200)
    #return JsonResponse({'people':'peoples_list'}, status = 200)

max_students = {'PUL':{'BCE':192, 'BCT':96, 'BEI':48, 'BEL':48, 'BAR':48,'BCH':48, 'BME':48},#'aerospace':48,
'THA':{'BCE':144, 'BCT':48, 'BEI':48, 'BAR':48, 'BME':48,'BIE':48, 'BAM':48 },
'PAS':{'BCE':144, 'BCT':48, 'BEI':48, 'BEL':48, 'BAM':48, 'BME':48,'BGE':48 },
'PUR':{'BCE':96, 'BCT':96, 'BEI':48, 'BEL':48, 'BAR':48, 'BME':96,'BAG':48 },
'KAT':{'BCE':96, 'BCT':96, 'BEI':96, 'BEL':48, 'BAR':48},
'KAN' : {'BCE':96, 'BCT':96, 'BEI':96},
'SEC' : {'BCE':48, 'BCT':48, 'BEI':48},
'ACE' : {'BCE':96, 'BCT':96, 'BEI':96, 'BEL':48},
'HCE' : {'BCE':96, 'BCT':48, 'BEI':48, 'BAR':48},
'NCE' : {'BCE':96, 'BCT':48, 'BEI':48, 'BEL':48},
'LEC' : {'BCE':48, 'BCT':48},
'KIC' : {'BCE':96, 'BCT':48, 'BEI':48},
'JAN' : {'BCE':96, 'BCT':48, 'BEI':48},
'KEC' : {'BCE':96, 'BCT':48, 'BEL':48},
'CHI' : {'BAR':24}}

def get_ioe_photos(request, collage, faculty, year_code):
    formats = ['jpg', 'jpeg', 'png']
    urls=[]
    for format in formats:
        urls.extend(['https://exam.ioe.edu.np/Images/StudentCurrentImage/3036/{}0{}{}{}.{}'.format(collage, year_code, faculty, f'{i:03}', format) for i in range(1,max_students[collage][faculty])])
    return render(request, 'person/ioe_images.html', {'urls':urls})

def get_ioe_photos_api(request, collage, faculty, year_code):
    formats = ['jpg', 'jpeg', 'png']
    urls=[]
    for format in formats:
        urls.extend(['https://exam.ioe.edu.np/Images/StudentCurrentImage/3036/{}0{}{}{}.{}'.format(collage.upper(), year_code, faculty.upper(), f'{i:03}', format) for i in range(1,max_students[collage][faculty])])
    return JsonResponse({'urls':urls}, status = 200)

def profile(request):
    print('\n\n profile invoked\n')
    if request.method == "GET":
        first_name = request.GET.get('first_name',None)
        last_name = request.GET.get('last_name',None)
        print("\n\n\nfirst_name: "+str(first_name) + "\n\nlast_name: " +str(last_name))
        people=[Person.objects.using('brainmap').filter(first_name=first_name, last_name=last_name)[0]]
    
        
    else:
        people='i want her';
        return JsonResponse({'people':people}, status = 200)
    
    return render(request, 'person/index.html', {'people':[people]})
    #return render(request, 'person/index.html', {'people':[people]})
    #people = serializers.serialize('json', [people], )
    #return JsonResponse({'people':people}, status = 200)
    
def search_em(request):
    print('\n\n search_section')
    if request.is_ajax and request.method == "GET":
        search_term = request.GET.get("search_term", None);
    return JsonResponse({'people':'peoples_list'}, status = 200)

#To get profile picture from tiktok
def get_profile_pic(person):
    print('getting profile pic of {}\n {}\n'.format(1,2))
    from bs4 import BeautifulSoup
    import requests
    URL = person.social_media_profiles[0]['tiktok']
    headers = {"user-agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
    page=requests.get(URL, headers=headers);
    soup = BeautifulSoup(page.content, 'html.parser');
    image = str(soup.find_all('img')[1]['src'])
    #image='Hi'
    return(image)

def edit_people(request):
    print('\n\n\neditig_people')
    if request.is_ajax and request.method == "POST":
        pass
    Person.objects.using('brainmap').get(id=id).update(empty_profile=False)

def add_people(request):
    print('\n\n\nadd_people')
    if request.is_ajax and request.method == "POST":
        #print('\n\ninn')
        person_form = PersonForm(request.POST)
        '''
        ################£££££££££££££££####################
        ################ Bring me back ####################
        ################£££££££££££££££####################
        
        if person_form.is_valid():
            print('valid person_form: ' + str(person_form))
            person_form.save()
        '''
        
        profile_pic = request.POST.get("profile_pic",None);
        
        first_name = request.POST.get("first_name");
        print(first_name)
        
        middle_name = request.POST.get("middle_name", '');
        print(middle_name)
        
        last_name = request.POST.get("last_name", '');
        print(last_name)
        
        gender = request.POST.get("gender", '');
        if str(gender.strip().lower()=='female'):
            gender='f'
        elif str(gender.strip().lower()=='male'):
            gender='m'
        else:
            gender=gender.strip().lower()
        print(gender)
        
        personality = request.POST.get("personality", '');
        print(personality)
        
        phone_number = request.POST.get("phone_number", 0);
        print(phone_number)

        religion = request.POST.get("religion", None);
        print(religion)
        
        country = request.POST.get("country", None);
        print(country)
        
        hobbies = request.POST.get("hobbies", None);
        print(hobbies)
        
        family_members = request.POST.get("family_members", None);
        print(country)
                
        education = request.POST.get("education", None);
        print(education)
            
        profession = request.POST.get("profession", None);
        print(profession)
        
        likes = request.POST.get("likes", []);
        print(likes)
        
        dislikes = request.POST.get("dislikes", []);
        print(dislikes)
        
        tags = request.POST.get("tags",)
        print(tags)
        
        social_media_profiles = request.POST.get("social_media_profiles",)
        print(social_media_profiles)
        
        smoke = request.POST.get("smoke", None);
        if (str(smoke).lower()=='false' or str(smoke).lower()=='f' or str(smoke).lower().startswith('n')):
            smoke = False;
        else:
            smoke = True;
        print(smoke)

        drink = request.POST.get("drink", None);
        if (str(drink).lower()=='false' or str(drink).lower()=='f' or drink == None  or str(drink)==''):
            drink = False;
        else:
            drink = True;
        print(drink)
        
        symbol = request.POST.get("symbol", None);
        p = Person.objects.using('brainmap').create(profile_pic=[profile_pic], first_name = first_name, middle_name = middle_name, last_name = last_name, gender = gender, profession = [profession], likes = [likes], dislikes = [dislikes], religion = religion, country = country, hobbies = [hobbies], family_members = [family_members], education = [education], smoke = smoke, drink = drink, rating = 10)
        for tag in tags:
            t=Tags(tag=tag, person = p)
            t.save()
        
        for url in social_media_profiles:
            s=SocialMedia(social_media_profile=s, person=p)
            s.save()
    
    return HttpResponseRedirect(reverse(index))
    #return JsonResponse({'people':'peoples_list'}, status=200)

'''Person.objects.using('brainmap').create(first_name='Dakshina', last_name="shrestha", emails=['dakshina@sagarmatha.edu.np'], gender = 'f', profession = ['Chief of Academics and Associate Professor at Sagarmatha Engineering College','Program Leader at Sagarmatha National College',], religion = 'hindu', country = 'nepal', education= ['Siddhartha Vanasthali Institute','Saint Xavier\'s College', 'Bangladesh University of Engineering and Technology (BUET)'], smoke = False,  rating = 10, tags = ['heroine','strict'],social_media_profiles= ['https://www.linkedin.com/in/dakshina-shrestha-1ba9669/', '', '' , '', '', '', 'https://www.facebook.com/dakshina.shrestha.3', '', '', '', '', '', '', '','', '', '', '','',])'''

def update_profile(request):
    print('\n\nupdate_profile invoked\n')
    if request.is_ajax and request.method == "POST":
        porfile_pic = request.POST.get("profile_pic", None);
        person_id = request.POST.get("persons_id", None);

    
    print('\n\nPerson id:{}\n'.format(person_id))
    
    print('\nProfile_pic:{}\n\n'.format(profile_pic))
    if (porfile_pic != None and person_id!=None):
        p= Person.objects.using('brainmap').get(id = int(persons_id))
        p.profile_pic = profile_pic
        p.save()
        return HttpResponse('Profile Pic Successfully saved')
    else:
        return HttpResponse('Profile Pic not saved persons_id:{}   profile_pic:{}'.format(persons_id, profile_pic))


def save_image_url(request):
    except_flag=False
    if request.is_ajax and request.method == "POST":
        # get the nick name from the client side.
        url = request.POST.get("url", None);
    if url!=None:
        ioe_roll_no = url.split('/')[-1].split('.')[0].lower()
        print('\nurl:[{}], ioe_roll_no:\'{}\'{}\n'.format(url, ioe_roll_no, len(ioe_roll_no)))
        try:
            p = Person.objects.using('brainmap').get(ioe_roll_no = str(ioe_roll_no))
        except:
            profile_exists_flag=True
            Person.objects.using('brainmap').create(profile_pic=[url], ioe_roll_no = ioe_roll_no,  empty_profile=True, profession=[str(ioe_roll_no[6:9]) + '_student'], sources=[], permanent_address=[], uses=[], social_engineering=[], location=[], phone_number=[], emails=[], adress=[], likes=[], dislikes=[], hobbies=[], family_members=[], education=[], symbols=[])
            print('\ncreated new url\n')
            return HttpResponse('Successfully created new url')
        if except_flag==False:            
            if p.profile_pic ==None:
            
                p.profile_pic=[url]
                p.save()
                print('\nadded url\n')
                return HttpResponse('Beep. Boop. Beep!! url added')
            elif str(url) not in p.profile_pic:
                p.profile_pic.append(url)
                p.save()
                print('\nadded url\n')
                return HttpResponse('Beep. Boop. Beep!! url added')
            else:
                print('\nurl already exist in the database\n')
                return HttpResponse('Beep. Boop. Beep!! image already exists, we don\'t have to add.')


########################################################################################################################################
#           --------------------------------------- To verify ioe user   -------------------------------------
########################################################################################################################################
#def each_data(ioe_roll_no = 'sec076bct028', last_name = 'baniya', dob_bs = '2058-12-04', dob_ad = '03/17/2002'):
def get_each_user(ioe_roll_no, last_name, dob_bs):#dob_ad
    # return None or data
    cookielib = http.cookiejar
    cj = cookielib.CookieJar()
    br = mechanize.Browser()
    br.set_cookiejar(cj)
    br.open("https://exam.ioe.edu.np/studentLogin/index")
    
    
    br.select_form(nr=0)
    br.form['CampusRollNumber'] = ioe_roll_no
    br.form['LastName'] = last_name
    br.form['DateOfBirth'] = dob_bs
    br.submit()
    
    '''
    br.open("https://entrance.ioe.edu.np/Home/ValidateStudent")
    
    br.select_form(nr=0)
    br.form['FormNo'] = '2076-10545'
    br.form['BirthDateBS'] = '2058/12/04'
    br.form['BirthDateAD'] = '03/17/2002'
    br.submit()
    '''
    #print(br.response().read())
    
    
    soup = BeautifulSoup(br.response().read())
    #print(soup)
    #print(soup.read())
    
    if 'The user is inactive' in str(soup.find_all('li')):
        print('\nInvalid_user:{}\n'.format(ioe_roll_no))
        return(None)
    else:
        
        img_url = 'https://exam.ioe.edu.np'+str(soup.find_all('img')[2]).split('\"')[5]
        
        categories = soup.find_all('h3')
        #try:
        categories.remove(categories[0])
        #except:
        #    return(None)
        
        data_names = soup.find_all('th')
        data_values = soup.find_all('td')
        
        #save = [{box_title[i]:{data_title[j]:all_data[j]}}] for i in range(0,len())
        # Data of each individual
        
        person = {}
        each_data = {}
        brkpts = [8,11,13,16]
        count=0
        
        
        for brk,category in enumerate(categories):
            for i in range(count,brkpts[brk]):
                
                #print('count:{}, brkpts[brk]:{}, i:{}'.format(count, brkpts[brk], i))
                each_data[data_names[i].get_text()]=data_values[i].get_text()
                count += 1
                if(i==brkpts[brk]):
                    count=i;
                    
                    
            #print(each_data)
            
            person[category.get_text()] = each_data
            each_data={}
            person['img_url'] = img_url
        return(person)
import datetime
from pyBSDate import convert_BS_to_AD, convert_AD_to_BS
def save(dta):
    first_name = dta['Personal Information:']['First Name'].lower()
    last_name = dta['Personal Information:']['Last Name'].lower()
    email = dta['Personal Information:']['Emailaddress'].lower()
    phone_number = [int(dta['Personal Information:']['Personal Contact Number'])]
    d = dta['Personal Information:']['Dob'].lower().split('-')
    d_ad=convert_BS_to_AD(int(d[0]), int(d[1]), int(d[2]))
    dob = datetime.date(d_ad[0], d_ad[1], d_ad[2])
    gender = dta['Personal Information:']['Gender'].lower()
    father  = dta['Personal Information:']['Father Name'].lower()
    #mother = dta['Personal Information:']['Emailaddress'].lower()
    collage = [dta['College Details:']['College '].lower()]
    
    ad = dta['College Details:']['Admission Date:'].lower().split('/')
    admission_date = datetime.date(int(ad[2]), int(ad[0]), int(ad[1]))
    #admission_date = convert_BS_to_AD(int(ad[2]), int(ad[0]), int(ad[1]))
    ioe_roll_no =  dta['College Details:']['College RollNo.'].lower()
    field_of_study = dta['Faculty Details:']['Field of Study:']
    degree = dta['Faculty Details:']['Degree']
    local_guardian = dta['Local Guardian']['Name']
    url = [dta['img_url']]
    try:
        local_guardian_telephone = [int(dta['Local Guardian']['Telephone'])]
    except:
        pass
    address = [dta['Local Guardian']['Address']]
    
    try:
        person = Person.objects.using('brainmap').get(ioe_roll_no=ioe_roll_no)
        person.first_name = first_name
        person.last_name = last_name
        if person.emails ==None:
            person.emails = [email]
        else:
            person.emails.append(email)
        
        if phone_number[0] not in person.phone_number:
            person.phone_number.append(phone_number[0])
        else:
            print('skipped phone_number')
        
        person.dob_ad=dob
        person.gender = gender
        person.education = collage
        person.location = address
        person.fathers_name = father
        person.field_of_study = field_of_study
        person.save()
        person.profile_pic = url
        person.degree = degree
        person.local_guardian = local_guardian
        
        try:
            person.local_guardian_telephone = local_guardian_telephone
        except:
            pass
        print('updating existing : {}'.format(first_name))
        person.save()
        
    except:
        print('creating new : {}'.format(first_name))
        a = Person.objects.using('brainmap').create(first_name = first_name, last_name = last_name, emails = [email], phone_number = phone_number, dob_ad=dob, gender = gender, education = collage, ioe_roll_no = ioe_roll_no, location = address,fathers_name = father, profession=str(ioe_roll_no[6:9]) + '_student')
        a.field_of_study = field_of_study
        a.degree = degree
        a.local_guardian = local_guardian
        try:
            a.local_guardian_telephone = local_guardian_telephone
        except:
            pass
        a.save()
@login_required
def verify(request, ioe_roll_no, last_name, dob_bs):
    ioe_data = get_each_user(ioe_roll_no, last_name, dob_bs)
    if ioe_data != None:
        save(ioe_data)
        print(ioe_roll_no, last_name, dob_bs)
        #return redirect('/chat')
        return HttpResponse(str(ioe_data) + str(ioe_roll_no)+ str(last_name)+ str(dob_bs))
        ########################################
        #redirect(password/username if password_not_set else redirect to email/phone verification)
        ########################################
    else:
        return HtttpResponse('Invalid credentials')
        ########################################
        #redirect(choose_username_and_password)
        ########################################

def login(request):
    if request.is_ajax and request.method == "GET":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None);
    if username != None and password != None:
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        #user.last_name = 'Lennon'
        user.save()
    else:
        return HttpResponse('username or password can\'t be blank')


#to edit
def edit(request):
    new_field = {}
    return HttpResponse('Saved successfully')

from django.contrib.auth import authenticate
def logins(request):
    user = authenticate(username='john', password='secret')
    if user is not None:
        # A backend authenticated the credentials
        pass
    else:
        pass
        # No backend authenticated the credentials

'''@login_required(login_url='/accounts/login/')
def profile(request):
    pass'''
    
########################################################################################################################################
#           /////////////////////////////////// To verify ioe user   //////////////////////////////////////////
########################################################################################################################################


def flush(request):
    # To flush the cache
    # This works as advertised on the memcached cache:
    cache.clear()
    return HttpResponse('cleared cache successfully')
    
    # This manually purges the SQLite cache:
    #cursor = connections['default'].cursor()
    #cursor.execute('DELETE FROM cache_table')
    #transaction.commit_unless_managed(using='cache_database')

#source /home/nathan/Documents/venv/bin/activate
#python3 manage.py shell
#from person.models import Person

#p.tags_set.all()

def ssl_cert(request):
    return HttpResponse('M58vqliMosBAdgOYNx9UW9DlcBQ71UIkaQ0YYWAq_zs.s1y7_YhjSk90w1NT8OBQ3LfEfRjn-eWv8R014Xl2Cco')
