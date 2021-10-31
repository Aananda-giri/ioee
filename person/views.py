from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import random

from django.template import loader

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


#from user.views import categoriesView

#780030519462
#780030523629
#OTP sent to Email: aanandaprashadgiri@gmail.com. Please enter valid OTP to submit application.
import json

from django.http import JsonResponse
from django.core import serializers




from .forms import PersonForm
from .models import Person

def index(request):
    people = [Person.objects.using('brainmap').all()[random.randint(0,29)]]
    '''stuti = Person.objects.using('brainmap').get(id=1)
    if(stuti.profile_pic == ''):
        stuti.profile_pic = get_profile_pic(stuti)
        stuti.save()
        print('pic:' + str(len(get_profile_pic(stuti))) + str(get_profile_pic(stuti)))
        print('\n\n Saved profile pic of  #',stuti.first_name)
        get_profile_pic(stuti)'''
    return render(request, 'person/index.html', {'people':people})


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

def profile(request):
    print('\n\n profile invoked\n')
    if request.method == "GET":
        first_name = request.GET.get('first_name',None)
        last_name = request.GET.get('last_name',None)
        print("\n\n\nfirst_name: "+str(first_name) + "\n\nlast_name: " +str(last_name))
        people=Person.objects.using('brainmap').filter(first_name=first_name, last_name=last_name)[0]
    
        
    else:
        people='i want her';
        return JsonResponse({'people':people}, status = 200)
    
    return render(request, 'person/index.html', {'people':[people]})
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


def add_people(request):
    print('\n\n\nadd_people')
    if request.is_ajax and request.method == "POST":
        print('\n\ninn')
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
        
        tags = request.POST.get("tags",);
        
        print(tags)
        
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
        Person.objects.using('brainmap').create(profile_pic=[profile_pic], first_name = first_name, middle_name = middle_name, last_name = last_name, gender = gender, profession = [profession], likes = [likes], dislikes = [dislikes], religion = religion, country = country, hobbies = [hobbies], family_members = [family_members], education = [education], smoke = smoke, drink = drink, rating = 10, tags = [tags])
        
        ''')'''
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
