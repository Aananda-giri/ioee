from django.http import JsonResponse
from django.core import serializers

from django.shortcuts import render
from api.data.ioe_crawler import run_spider
import json


# runs spider - save first page of exam.ioe.edu.np to new_notices.json
def get_new_notifications(request):
    run_spider()
    notifications = get_notifications()
    #notifications = serializers.serialize('json', notifications, )
    print('notifications')
    return JsonResponse({'notices':notifications}, status = 200)
    #return notifications

#nnot = get_new_notification('req')
#print('\n\n\n Notifications:' +  str(nnot) +'\n\n\n')


# gets new notices from new_notices.json using notices.json
# return new notices
# add new notices to notices.json
def get_notifications(what=None):
    with open('api/data/notices.json', 'r') as file:
      old_notices = json.load(file)
    
    with open('api/data/new_notices.json', 'r') as file:
      newly_scrapped = json.load(file)
    new_notices = []
    
    #reversed because it would be easier to stack on top of old_data
    #scraped_topics.reverse()
    #scraped_urls.reverse()
    
    
    for index, notice in enumerate(reversed(newly_scrapped)):
      if notice not in old_notices:
          old_notices.insert(0, notice)
          new_notices.insert(0, notice)
          print('Adding new notices:\n\t {}'.format(new_notices))
    
    with open('api/data/notices.json','w') as file:
      json.dump(old_notices, file, indent = 4)
    
    ## Got new_topics and new_urls
    if what !=None:print(what)
    #print(new_notices)
    return(new_notices)

def get_saved_notifications(request, how_many:int):
    #if int(how_many>50):
    #    how_many = 50
    with open('api/data/ioe_notices.json', 'r') as file:
      notices = json.load(file)
    notices = notices[:how_many]
    #notifications = {'topics':topics, 'urls':urls}
    return JsonResponse({"notices":notices}, status = 200)
