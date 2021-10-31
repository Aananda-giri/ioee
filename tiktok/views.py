from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.http import JsonResponse
import os, time

# Create your views here.

def get_tiktok_s_v_web_id(request):
    
    #driver = webdriver.Firefox()
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options)
    
    
    
    
    s_v_web_id = None
    driver.get("http://www.tiktok.com")
    print('sleeping 5 seconds')
    time.sleep(8)
    cookies = driver.get_cookies()
    for cookie in cookies:
        if cookie['name']=='s_v_web_id':
            s_v_web_id = cookie['value']
    
    if s_v_web_id != None:
        #Sends {'s_v_web_id':s_v_web_id} if unable to get s_v_web_id
        return JsonResponse({'s_v_web_id':s_v_web_id}, status=200)
    else:
        return JsonResponse({'cookies':cookies}, status=200)
