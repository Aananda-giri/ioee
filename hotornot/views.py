from django.shortcuts import render, HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
#import base64
#import requests
from .models import Person, RoundFemale, RoundMale, Feedbacks

from django.urls import reverse

import random
import math

import json
from django.http import JsonResponse
from django.core import serializers
import threading

# Create your views here.

'''def get_data_urls(urls):
    data_urls = []
    for url in urls:
        response = requests.get(url)
        content_type = response.headers["content-type"]
        encoded_body = base64.b64encode(response.content)
        u = "data:{};base64,{}".format(content_type, encoded_body.decode())
        data_urls.append(u)
        
    return(data_urls)'''

def get_level(voted_people_of_level, total_people_of_level):
    #To determine Round_id
    
    for l,n in enumerate(total_people_of_level):
        #print('l:{}  no_of_poople:{} total_people_of_level:{}'.format(l,no_of_poople, type(voted_people_of_level)))
        
        try:
            #print('\ntry\n')
            #print('\nTrying:{}\n'.format(voted_people_of_level[l] < no_of_people))
            if(voted_people_of_level[l] < n):level = l
            #print('level:{}'.format(level))
        except:
            break
    return(level)


def createNewRound(total_people, Round, round_id, min_id, max_id):
    print('\n\n\nCreating new round with Round_id: {} min_id: {} max_id: {}  total_people:{}\n\n'.format(round_id,min_id, max_id, total_people))
    temp = total_people
    total_people_of_level = [temp]
    while(total_people_of_level[-1]!=1):
        t2=math.ceil(temp/2)
        total_people_of_level.extend([t2])
        temp=t2
    
    r = Round.objects.using('hotornot').create(id = round_id)
    r.total_people_of_level = total_people_of_level
    r.voted_people_of_level = [0]
    r.unranked_ids = [i for i in range(min_id, max_id+1)]
    r.ranked_ids = []
    r.save()

def createNewLevel(Round, round_id, unranked_ids):
    r= Round.objects.using('hotornot').filter(id=round_id)[0]
    r.voted_people_of_level.append(0)
    r.ranked_ids = []
    r.unranked_ids = unranked_ids
    r.save()

def get_and_save_random_pair(unranked_ids, Round, round_id):
    #Getting all the random unranked ids and storing them to database
    random_pairs = random.sample(unranked_ids, math.floor(len(unranked_ids)/2))
    print('\nrandom_pairs: {}\n'.format(random_pairs))
    
    r = Round.objects.using('hotornot').get(id=round_id)
    
    # first and second elements of random_pair are round_id and level respectively
    #random_pairs.insert(0, round_id)
    #random_pairs.insert(1, level)
    
    r.random_pairs = random_pairs
    r.save()
    return(random_pairs)

def update_rounds_and_datas(gender):
    '''#data=get_data_url(Person.objects.using('hotornot').filter(gender='f')[3].url_base+Person.objects.using('hotornot').all().filter(gender='f')[3].ioe_roll_no+'.'+Person.objects.using('hotornot').all().filter(gender='f')[3].image_format)
    
    people = Person.objects.using('hotornot').filter(gender=gender)
    #max=len(prople)
    if gender=='f':
        min_id = 0
        max_id = 1449
        total_people = 1450
        Round = RoundFemale
        #return HttpResponse('Hello World')        
    elif gender =='m':
        min_id = 1450
        max_id = 8109
        total_people = 6660
        Round = RoundMale
    else:
        return HttpResponseRedirect(reverse(gender,args=('f')))
        
    total_ids = [i for i in range(min_id, max_id + 1)]
    random_pairs = random.sample(total_ids, 2)
    [total_ids.remove(i) for i in random_pairs]
    #print(random_pairs)
    urls=[]
    for i in random_pairs:
        urls.append(Person.objects.using('hotornot').filter(id=i)[0].url_base+Person.objects.using('hotornot').all().filter(id=i)[0].ioe_roll_no+'.'+Person.objects.using('hotornot').all().filter(id=i)[0].image_format)
    round_id=0
    return render(request, 'hotornot/index.html', {'urls':urls, 'round_id':round_id, 'random_pairs':random_pairs})
    #return HttpResponse('Hello World'+str(urls))
    
    #data_urls = get_data_urls(urls)

    
#ranked_ids = get_ranked_ids()'''










    if gender=='f':
        min_id = 0
        max_id = 1449
        total_people = 1450
        Round = RoundFemale
        #return HttpResponse('Hello World')        
    elif gender =='m':
        min_id = 1450
        max_id = 8109
        total_people = 6660
        Round = RoundMale
    else:
        return HttpResponseRedirect(reverse(gender, args=('f')))
        
    
    round_id = len(Round.objects.using('hotornot').all())-1
    
    if(round_id==-1):
        # Initially At the launch of website
        createNewRound(total_people, Round, round_id+1, min_id, max_id)
        round_id = len(Round.objects.using('hotornot').all()) - 1

    print('\n\nRound_id ={}\n'.format(round_id))
    #Total no. of people that will vote in each seperate round
    #female:[1450, 725, 363, 182, 91, 46, 23, 12, 6, 3, 2, 1],male:[6660, 3330, 1665, 833, 417, 209, 105, 53, 27, 14, 7, 4, 2, 1]
    total_people_of_level = Round.objects.using('hotornot').filter(id=round_id)[0].total_people_of_level
    print('\ntotal_people_of_level:{}\n'.format(total_people_of_level))
    
    #shows progress of current voting
    #eg. [1450, 102]    102 is currently filling
    voted_people_of_level = Round.objects.using('hotornot').filter(id=round_id)[0].voted_people_of_level
    print('\nvoted_people_of_level: {}\n'.format(voted_people_of_level))
    
    level = get_level(voted_people_of_level, total_people_of_level)
    print('\nlevel: {}\n'.format(level))
    
    #List of ranked ids
    ranked_ids = Round.objects.using('hotornot').filter(id=round_id)[0].ranked_ids
    print('\nranked_ids: {}\n'.format(ranked_ids))
    
    #List of unranked ids
    unranked_ids = Round.objects.using('hotornot').filter(id=round_id)[0].unranked_ids
    print('\nunranked_ids: {}\n'.format(unranked_ids))




    random_pairs = get_and_save_random_pair(unranked_ids= unranked_ids, Round = Round, round_id = round_id)
    
    
    #urls=[]
    #for i in random_pairs:
    #    urls.append(Person.objects.using('hotornot').filter(id=i)[0].url_base+Person.objects.using('hotornot').all().filter(id=i)[0].ioe_roll_no+'.'+Person.objects.using('hotornot').all().filter(id=i)[0].image_format)














    if len(unranked_ids)<2:
        # i.e. current level is completed
        
        if( len(voted_people_of_level) == len(total_people_of_level)):
            #i.e.current round is completed
            createNewRound(total_people, Round, round_id, min_id, max_id)
        
        else:
            #i.e. current level is full
            unranked_tuples = Person.objects.using('hotornot').filter(gender='gender').order_by('-votes')[:total_people_of_level[level]].values_list('id')
            
            unranked_ids=[i[0] for i in unranked_tuples]
            
            createNewLevel(Round=Round, round_id=round_id, unranked_ids=unranked_ids)


    return(random_pairs)
    
    #return render(request, 'hotornot/index.html', {'urls':urls, 'round_id':round_id, 'random_pairs':random_pairs[:2], 'level':level})
    
    
    
    
    
    
        
        #data_urls = get_data_urls(urls)
    #return render(request, 'hotornot/index.html', {'data_urls':data_urls, 'round_id':round_id, 'random_pairs':random_pairs})
    ''''''
    
    
    
    '''
    select = random.sample(unranked_ids,2)
    ranked_ids.extend(select)
    [ unranked_ids.remove(i) for i in selected_ids ]
    
    temp = total_people
    total_people_of_level = [temp]
    while(total_people_of_level[-1]!=1):
        t2=int(temp/2)
        total_people_of_level.extend([t2])
        temp=t2
    '''
    '''   try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})'''
    #return HttpResponse('Hello World')
    #return render(request, 'hotornot/index.html', {'data_urls':data_urls})



def gender_details(request, gender='f'):
    #return render(request, 'hotornot/index.html')
    send_via_json = False
    
    if request.is_ajax and request.method == "GET":
        # get the nick name from the client side.
        send_via_json = bool(request.GET.get("json", False))
        
        #Because otherwise this code will excute whether or not jsonrequest
        if send_via_json==True:
            gender = request.GET.get("gender", 'f')
        
        
    #print('\n\njoke_id:' + str(int(joke_id)))
    
    if gender=='m':
        Round = RoundMale
    else:
        Round = RoundFemale
    
    round_id = len(Round.objects.using('hotornot').all())-1
    if round_id==-1:
        update_rounds_and_datas(gender)
        round_id = len(Round.objects.using('hotornot').all())-1
    print('round_id:{}'.format(round_id))
    

    random_pairs = Round.objects.using('hotornot').filter(id=round_id)[0].random_pairs

    #random_pairs = get_and_save_random_pair(unranked_ids= unranked_ids, Round = Round, round_id = round_id)    
    
    if (len(random_pairs)<2):
        update_rounds_and_datas(gender)
    elif (len(random_pairs)>100):
        random_pairs = random_pairs[:100]
    
    url_base = 'https://exam.ioe.edu.np/Images/StudentCurrentImage/3030/'
    ioe_roll_no_tuple = Person.objects.using('hotornot').filter(id__in=random_pairs).values_list('ioe_roll_no_with_format')
    ioe_roll_no = [i[0] for i in ioe_roll_no_tuple]
    
    #print(ioe_roll_no)
    #print(type(ioe_roll_no)==type(random_pairs))
    if send_via_json==True:
        print('\nSend VIA JSON')
        return JsonResponse({'random_pairs':random_pairs, 'url_base' : url_base, 'ioe_roll_no' : ioe_roll_no, 'round_value':'true', 'round_id':round_id, 'gender':gender },status=200)
    else:
        print('Send VIA render:{}'.format(type(send_via_json)))
        return render(request, 'hotornot/index.html', {'random_pairs':random_pairs, 'url_base' : url_base, 'ioe_roll_no' : ioe_roll_no, 'round_value':'true', 'round_id':round_id, 'gender':gender})

#comments = serializers.serialize('json', comments, )

    

def collage_faculty_details(request):
    #return render(request, 'hotornot/index.html')
    send_via_json = False
    
    if request.is_ajax and request.method == "GET":
        # get the nick name from the client side.
        gender = request.GET.get("gender", 'f')
        collage = request.GET.get("collage", None)
        faculty = request.GET.get("faculty", None)
        top_hundred = request.GET.get("top_hundred", None)
        
        send_via_json = bool(request.GET.get("send_via_json", False))
    print('\ngender:{} gender==\'Gender\':{}, Collage:{}  collage=\'Collage\':{}, faculty:{} faculty==\'Faculty\':{}, send_via_json'.format(gender, gender=='Gender', collage, collage=='Collage', faculty, faculty=='Faculty', send_via_json))
    
    
    if gender=='m':
        Round = RoundMale
    else:
        Round = RoundFemale
        gender = 'f'
    
    #round_id = len(Round.objects.using('hotornot').all())-1
    #if round_id==-1:
    #    update_rounds_and_datas(gender)
    
    #print('round_id:{}'.format(round_id))
    
    
    # Collage for json and None for http://127.0.0.1:8000/h/collage/
    if collage=='Collage' or collage==None:
        print("\ncollage==''\n")
        if faculty != 'Faculty' and faculty != None:
            #print("\ncollage==''    faculty = {} type:{}\n".format(faculty, type(faculty)))
            print('faculty is given')
            people = Person.objects.using('hotornot').filter(gender=gender,faculty=faculty ).order_by('votes').values_list('id', 'ioe_roll_no_with_format')
            #people = list(people)
            
        else:
            print('\n\n\n else1')
            return HttpResponseRedirect(reverse(gender_details, args=['f']))
    
    
    elif faculty=='Faculty'  or faculty==None:
        
        if collage != 'Collage' and collage != None:
            #print("\nfaculty == ''     collage!==''    \n")
            print('collage is given',type(gender))
            
            people = Person.objects.using('hotornot').filter(gender=gender, collage=collage ).order_by('-votes').values_list('id', 'ioe_roll_no_with_format')
            #print(people)
            #people = list(people)
            
        else:
            return HttpResponseRedirect(reverse(gender_details, args=['f']))
            print('\n\n\n else2')
            
    
    
    else:
        #i.e. faculty and collage values are given
        #print("\nfaculty == ''     collage!==''    \n")
        print('collage and faculty are given')
        people = Person.objects.using('hotornot').filter(gender=gender, collage=collage ).order_by('-votes').values_list('id', 'ioe_roll_no_with_format')
        
        
    
    people = list(people)
    if (top_hundred != 'true'):
        random.shuffle(people)
    random_pairs = []
    ioe_roll_no = []
    for person in people:
        random_pairs.append(person[0])
        ioe_roll_no.append(person[1])
    
    #To get even no. of people as comparision will require even no of images
    even_length = math.floor((len(random_pairs)/2)*2)
    
    #To get only 50 pairs at a time
    if even_length>100:
        even_length=100
    
    print('\n\neven_length:{} len(random_pairs):{}\n'.format(even_length, len(random_pairs)))
    random_pairs = random_pairs[:even_length]
    ioe_roll_no = ioe_roll_no[:even_length]
    print(random_pairs)
    url_base = 'https://exam.ioe.edu.np/Images/StudentCurrentImage/3030/'
    round_id = len(Round.objects.using('hotornot').all())-1
    print('round_id:{}'.format(round_id))
    
    if send_via_json==True:
        print('GET VIA JSON so SENDING via json')
        return JsonResponse({'random_pairs':random_pairs, 'url_base' : url_base, 'ioe_roll_no' : ioe_roll_no, 'round_value':'false', 'round_id':round_id, 'gender':gender },status=200)
    else:
        print('GET VIA request so SENDING via json')
        return render(request, 'hotornot/index.html', {'random_pairs':random_pairs, 'url_base' : url_base, 'ioe_roll_no' : ioe_roll_no, 'round_value':'false', 'round_id':round_id, 'gender':gender})


def test(request):
    return HttpResponseRedirect(reverse(gender, args=('f')))
def collage_details(request, collage):
    return HttpResponse('Hello World from collage_details')
    #return render(request, 'hotornot/index.html', {'data_urls':data_urls})


def polls(request):
    formatt=['tif','tiff','gif','eps','raw']
    rollno = [f'{i:03}' for i in range(1,50)]
    serial=[i for i in range(3000,3100)]
    return render(request, 'hotornot/polls.html',{'rollno':rollno,'format':formatt,'serial':serial})

def vote(request):
    print('\n\nVoting image\n\n')
    if request.is_ajax and request.method == "POST":
        id1 =  int(request.POST.get('id1'))
        id2 =  int(request.POST.get('id2'))
        voted_id= int(request.POST.get('voted_id'))
        round_id = int(request.POST.get('round_id'))
        gender = request.POST.get('gender')
        round_value = request.POST.get('round_value', False)
    
    
    if(gender=='gender'):
        gender = 'f'
        Round = RoundFemale
    elif(gender=='f'):
        Round = RoundFemale
    elif(gender=='m'):
        Round = RoundMale
    else:
        return HttpResponseRedirect(reverse(gender, args=('f')))
        #return HttpResponseRedirect(reverse(gender))
    
    print('gender:{}  ids:{},{} voted:{} round_id:{} round_value:{}'.format(gender, id1, id2, voted_id, round_id, round_value))
    
    print('ids:{},{} voted:{}'.format(id1, id2, voted_id))
    #Updating votes and views
    p1 = Person.objects.using('hotornot').get(id=id1)
    p1.views += 1
    p1.save()
    
    p2 = Person.objects.using('hotornot').get(id=id2)
    p2.views += 1
    p2.save()
    
    p3 = Person.objects.using('hotornot').get(id=voted_id)
    p3.votes += 1
    p3.save()
    
    if round_value=='true':
        #updating ranked ana unranked_ids
        r=Round.objects.using('hotornot').get(id=round_id)
        r.voted_people_of_level[int(round_id)] += 1
        #r.ranked_ids.extend([id1,id2])
        
        try:
            [r.unranked_ids.remove(i) for i in [id1, id2] ]
        except:
            print('\n\n\n Passing to remove from unranked_ids');
            pass
        try:
            [r.random_pairs.remove(i) for i in [id1,id2]]
        except:
            print('\n\n\n Passing to remove from random_pairs');
            pass
        r.save()
    return HttpResponse('Votes Saved')

def gender_only(request):
        #return render(request, 'hotornot/index.html')
    send_via_json = False
    
    if request.is_ajax and request.method == "GET":
        # get the nick name from the client side.
        gender = request.GET.get("gender", 'f')
        
        
        #send_via_json = bool(request.GET.get("send_via_json", False))
    #print('\ngender:{} gender==\'Gender\':{}, Collage:{}  collage=\'Collage\':{}, faculty:{} faculty==\'Faculty\':{}, send_via_json'.format(gender, gender=='Gender', collage, collage=='Collage', faculty, faculty=='Faculty', send_via_json))
    
    
    if gender=='m':
        Round = RoundMale
    else:
        Round = RoundFemale
        gender = 'f'
    
    #round_id = len(Round.objects.using('hotornot').all())-1
    #if round_id==-1:
    #    update_rounds_and_datas(gender)
    
    #print('round_id:{}'.format(round_id))
    people = Person.objects.using('hotornot').filter(gender=gender).order_by('?').values_list('id', 'ioe_roll_no_with_format')
    people = random.shuffle(people)
    
    
    
    random_pairs = []
    ioe_roll_no = []
    for person in people:
        random_pairs.append(person[0])
        ioe_roll_no.append(person[1])
    
    #To get even no. of people as comparision will require even no of images
    even_length = math.floor((len(random_pairs)/2)*2)
    
    #To get only 50 pairs at a time
    if even_length>100:
        even_length=100
    
    print('\n\neven_length:{} len(random_pairs):{}\n'.format(even_length, len(random_pairs)))
    random_pairs = random_pairs[:even_length]
    ioe_roll_no = ioe_roll_no[:even_length]
    print(random_pairs)
    url_base = 'https://exam.ioe.edu.np/Images/StudentCurrentImage/3030/'
    round_id = len(Round.objects.using('hotornot').all())-1
    print('round_id:{}'.format(round_id))
    
    if send_via_json==True:
        print('GET VIA JSON so SENDING via json')
        return JsonResponse({'random_pairs':random_pairs, 'url_base' : url_base, 'ioe_roll_no' : ioe_roll_no, 'round_value':'false', 'round_id':round_id, 'gender':gender },status=200)
    else:
        print('GET VIA request so SENDING via json')
        return render(request, 'hotornot/index.html', {'random_pairs':random_pairs, 'url_base' : url_base, 'ioe_roll_no' : ioe_roll_no, 'round_value':'false', 'round_id':round_id, 'gender':gender})

def total_views_and_votes():
    votes = 0
    views = 0
    people = Person.objects.using('hotornot').filter(views__gte = 1).values_list('views', 'votes')
    for person in people:
        votes += person[1]
        views += person[0]
    return({'views':views, 'votes':votes})

def feedback(request):
    
    body=''
    if request.is_ajax and request.method == "POST":
        
        username = request.POST.get('username','')
        body = request.POST.get('feedback','')
        #summary = request.POST.get('summary')
        email = request.POST.get('email')
        
        print('\nbody:{} username:{} email:{}'.format(body, username, email))
    
    if (body!='' and username!=''):
        Feedbacks.objects.using('hotornot').create(username=username, body=body, email=email)
        
        print('feedback saved')
        feedbacks = list(Feedbacks.objects.using('hotornot').all().values_list('username', 'body'))[-1:]#serializers.serialize('json', list(Feedback.objects.all().values_list('username', 'body'))[-1:], )
        return JsonResponse({"Saved":True,'feedbacks':feedbacks}, status = 200)
    
    
    else:
        feedbacks = Feedbacks.objects.using('hotornot').all().order_by('-pub_date').values_list('username', 'body')
        #print(feedbacks)
        return render(request, 'hotornot/feedbacks.html', {'feedbacks':feedbacks})

def fuse_attend(request):
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import time
    driver = webdriver.Firefox()
    
    # opens url
    driver.get('https://sagarmatha.student.fuseclassroom.com/login')
    
    # to make sure pag is opened throws AssertionError if false
    assert "Education Platform | Fuse Classroom" in driver.title
    
    print('\n\n\nEntering username and passwords:\n\n\n')
    time.sleep(5)
    
    # Finds element bu name
    username = driver.find_element_by_name("username")
    username.clear()
    username.send_keys('076bei001.aananda@sagarmatha.edu.np')
    
    password = driver.find_element_by_name("password")
    password.clear()
    password.send_keys('qLVViSLzCp3SeGK')
    
    # submits form (enter key?)
    password.send_keys(Keys.RETURN)
    
    print('\n\n\nSleeping 15 seconds after submitting password:\n\n\n')
    time.sleep(15)
    
    
    assert "No results found." not in driver.page_source
    driver.get("https://sagarmatha.student.fuseclassroom.com/live-class/schedule")
    
    print('\n\n\nSleeping 5 seconds before clicking "JOIN CLASS":\n\n\n')
    time.sleep(5)
    
    try:
    
        # gets element by class name
        live_class = driver.find_element_by_class_name("btn-success")
        live_class.click()
        return HttpResponse('Successfully attended.')
    except:
        print('Live Class not started')
        return HttpResponse('Live Class not started')
    
    copy_btn = driver.find_element_by_class_name("copy")
    copy_btn.click()
    
    print('\n\n\n Your attendence is successfully done:\n\n\n')
    time.sleep(5)
    
    driver.close()
    driver.quit()

def send_http_response(response): 
    return HttpResponse(response)

def fuse_attendd(request):
    #message = 'hi'
    #t2 = threading.Thread(target = send_http_response, args = (message,))
    #t2.setDaemon(True)
    #t2.start()
    #return HttpResponse('lol')
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import os
    import time
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options)
    
        # opens url
    driver.get('https://sagarmatha.student.fuseclassroom.com/login')
    
    # to make sure pag is opened throws AssertionError if false
    assert "Education Platform | Fuse Classroom" in driver.title
    
    print('\n\n\nEntering username and passwords:\n\n\n')
    time.sleep(3)
    
    # Finds element bu name
    username = driver.find_element_by_name("username")
    username.clear()
    username.send_keys('076bei001.aananda@sagarmatha.edu.np')
    
    password = driver.find_element_by_name("password")
    password.clear()
    password.send_keys('qLVViSLzCp3SeGK')
    
    # submits form (enter key?)
    password.send_keys(Keys.RETURN)
    
    
    message = '\n\n\nSleeping 2 seconds after submitting password:\n\n\n'
    print(message)
    #t1 = threading.Thread(target = send_http_response, args = (message,))
    #t1.setDaemon(True)
    #t1.start()
    time.sleep(2)
    
    
    assert "Education" in driver.title
    driver.get("https://sagarmatha.student.fuseclassroom.com/live-class/schedule")
    
    message='\n\n\nSleeping 2 seconds before clicking "JOIN CLASS":\n\n\n'
    print(message)
    #t2 = threading.Thread(target = send_http_response, args = (message,))
    #t2.setDaemon(True)
    #t2.start()
    time.sleep(2)
    
    try:
    
        # gets element by class name
        live_class = driver.find_element_by_class_name("btn-success")
        live_class.click()
        message = '\n\n\n Your attendence is successfully done\n\n\n'#.format(str(sub))
    except:
        message = 'Live Class not started'
    
    driver.close()
    driver.quit()
    #t3 = threading.Thread(target = send_http_response, args = (message,))
    #t3.setDaemon(True)
    #t3.start()
    return HttpResponse(message+' wew')
    #copy_btn = driver.find_element_by_class_name("copy")
    #copy_btn.click()
    
    #time.sleep(5)
