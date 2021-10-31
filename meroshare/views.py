from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Person
# Create your views here.

def index(request):
    username=None
    if request.is_ajax and request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
    
    if username != None and password != None:
        p = Person.objects.using('fuse_attend').create(username=username, password=password, login_url = 'https://sagarmatha.student.fuseclassroom.com/login')
        return HttpResponse('.add_user ' + str(p.auto_pseudoid))
    else:
        return render(request, 'fuse_attend/index.html')
        #HttpResponse('Username/Password can\'t be Null')

def fuse_attend(request, username):
    
    try:
        user = Person.objects.using('fuse_attend').filter(auto_pseudoid = str(username).strip())[0]
        usr_username = user.username
        usr_password = user.password
    except:
        return HttpResponse('username:"{}" \n User not registered'.format(username))
    #return HttpResponse('hi')
    #message = 'hi'
    #t2 = threading.Thread(target = send_http_response, args = (message,))
    #t2.setDaemon(True)
    #t2.start()
    #return HttpResponse('lol')
    
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import os
    import time
    #driver = webdriver.Firefox()
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options)
    
        # opens url
    driver.get('https://sagarmatha.student.fuseclassroom.com/login')
    
    print('\n\n\nEntering username and passwords (sleep 12 sec.):\n\n\n')
    time.sleep(7)
        
    # to make sure pag is opened throws AssertionError if false
    assert "Education Platform | Fuse Classroom" in driver.title
    
    
    
    # Finds element bu name
    username = driver.find_element_by_name("username")
    username.clear()
    username.send_keys(usr_username)            #'076bei001.aananda@sagarmatha.edu.np')
    
    password = driver.find_element_by_name("password")
    password.clear()
    password.send_keys(usr_password)            #'qLVViSLzCp3SeGK')
    
    # submits form (enter key?)
    password.send_keys(Keys.RETURN)
    
    
    message = '\n\n\nSleeping 5 seconds after submitting password:\n\n\n'
    print(message)
    #t1 = threading.Thread(target = send_http_response, args = (message,))
    #t1.setDaemon(True)
    #t1.start()
    time.sleep(3)
    
    
    
    driver.get("https://sagarmatha.student.fuseclassroom.com/live-class/schedule")
    
    #assert "My Classroom All Apps" in driver.body
    #if "Live Class" in driver.page_source:
    #    print("\n\nMy Classroom All Apps\n\n")
    #else:
    #    print('\n\n\n\n\n' + str(driver.page_source) + '\n\n\n')
    
    message='\n\n\nSleeping 5 seconds before clicking "JOIN CLASS":\n\n\n'
    print(message)
    #t2 = threading.Thread(target = send_http_response, args = (message,))
    #t2.setDaemon(True)
    #t2.start()
    time.sleep(3)
    
    try:
        sub=driver.find_element_by_class_name("text-success").text
        # gets element by class name
        live_class = driver.find_element_by_class_name("btn-success")
        live_class.click()
        message = '\n\n\n Your attendence is successfully done: \"{}\" \n\n\n'.format(str(sub))
    except:
        message = 'Live Class not started'
    
    driver.close()
    driver.quit()
    #t3 = threading.Thread(target = send_http_response, args = (message,))
    #t3.setDaemon(True)
    #t3.start()
    print(message)
    return HttpResponse(message)
    #copy_btn = driver.find_element_by_class_name("copy")
    #copy_btn.click()
    
    #time.sleep(5)
