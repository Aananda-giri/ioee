from django.http import JsonResponse
from django.core import serializers

from django.shortcuts import render
from api.data.ioe_crawler import run_spider
import json


# Create your views here.

def get_new_notifications(request):
    run_spider()
    notifications = get_notifications()
    #notifications = serializers.serialize('json', notifications, )
    print('notifications')
    return JsonResponse(notifications, status = 200)
    #return notifications

#nnot = get_new_notification('req')
#print('\n\n\n Notifications:' +  str(nnot) +'\n\n\n')


def get_notifications(what=None):
    with open('api/data/ioe_notices.json', 'r') as file:
      data = json.load(file)

    old_topics = data['topics']
    old_urls = data['urls']

    with open('api/data/new_notices.json', 'r') as file:
      new = json.load(file)

    scraped_topics = new['topics']
    scraped_urls = new['urls']

    #reverse because it would be easier to stack on top of old_data
    scraped_topics.reverse()
    scraped_urls.reverse()
    
    new_topics = []
    new_urls = []

    for i, nu in enumerate(scraped_urls):
      if nu not in old_urls:
          old_urls.insert(0, nu)
          old_topics.insert(0, scraped_topics[i])
          new_topics.insert(0, scraped_topics[i])
          new_urls.insert(0, nu)
          print('Adding new:\n\t topic {}\n\t url:{}'.format(scraped_topics[i], nu))

    with open('api/data/ioe_notices.json','w') as file:
      json.dump({'topics':old_topics, 'urls':old_urls}, file, indent = 4)

    ## Got new_topics and new_urls
    if what !=None:print(what)
    print({'topics':new_topics, 'urls':new_urls})
    return({'topics':new_topics, 'urls':new_urls})

def get_saved_notifications(request, how_many:int):
    if int(how_many>15):
        how_many = 15
    with open('api/data/ioe_notices.json', 'r') as file:
      data = json.load(file)
    topics = data['topics'][:how_many]
    urls = data['urls'][:how_many]
    notifications = {'topics':topics, 'urls':urls}
    return JsonResponse(notifications, status = 200)
