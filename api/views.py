from django.http import JsonResponse
from django.core import serializers

from django.shortcuts import render
from api.data.ioe_crawler import run_spider
from api.models import IoeNoti
import json




# runs spider - save first page of exam.ioe.edu.np to new_notices.json
def new_notifications_view(request):
    run_spider()    #saves scraped notices to api/data/new_notices.json
    unique_new_notices = filter_new_from_old_notices()   # returns unique_new notices
    print('notifications')
    return JsonResponse({'notices':unique_new_notices}, status = 200)
    #return notifications

#nnot = get_new_notification('req')
#print('\n\n\n Notis:' +  str(nnot) +'\n\n\n')


# gets new notices from new_notices.json using notices.json
# return new notices
# add new notices to notices.json
def filter_new_from_old_notices():
    with open('api/data/new_notices.json', 'r') as file:
        newly_scrapped = json.load(file)
    unique_new = []
    
    # checking if notices already exist in database
    for notice in reversed(newly_scrapped):
        print(notice['title'])
        if not IoeNoti.objects.filter(title=notice['title'], url=notice['url'], date=notice['date']).exists():
            print('\nadding\n')
            unique_new.append(notice)
    
    if unique_new!=[]:
        notices_count = IoeNoti.objects.all().count()
        IoeNoti.objects.bulk_create([IoeNoti(title=notice["title"], url=notice["url"], date=notice["date"], id = n + notices_count) for n, notice in enumerate(unique_new)])
        print('\nsaved\n')
        # store to database if unique_new notices list not empty
        
    print(unique_new)
    return(unique_new)



def get_saved_notifications(request, how_many:int):
    #if int(how_many>50):
    #    how_many = 50
    
    # Approach_1: Faster
    notices_count = IoeNoti.objects.all().count()
    notices = IoeNoti.objects.all()[notices_count - how_many -1 : notices_count-1].values_list() # gets latest 'how_many' notices
    
    # Approach_2: Slower
    #notices = IoeNoti.objects.all().order_by("-id")[:300]
    
    return JsonResponse({"notices":notices}, status = 200, safe=False)

'''        notices_count = IoeNoti.objects.all().count()
    notices = IoeNoti.objects.all().order_by('id')[notices_count - how_many -1 : notices_count-1] # gets latest 'how_many' notices
    notices = serializers.serialize('json',notices)'''


from api.models import IoeNoti
from api.serializers import NotiSerializer
from rest_framework import generics

from rest_framework import permissions
from api.permissions import IsOwnerOrReadOnly

class NotiList(generics.ListCreateAPIView):
    queryset = IoeNoti.objects.using('fuse_attend').all()
    serializer_class = NotiSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class NotiDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = IoeNoti.objects.using('fuse_attend').all()
    serializer_class = NotiSerializer
    
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
