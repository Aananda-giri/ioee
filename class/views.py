from django.shortcuts import render, HttpResponse
from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse
from hotornot.models import Person

import random
import math

import json
from django.http import JsonResponse
from django.core import serializers
import threading

collages = ['PUL', 'THA', 'PAS', 'PUR', 'KAT', 'KAN', 'SEC', 'ACE', 'HCE', 'NCE', 'LEC', 'KIC', 'JAN', 'KEC', 'CHI']

faculties = ['BCE', 'BCT', 'BEI', 'BAR', 'BME', 'BEL', 'BCH', 'BIE', 'BAM', 'BGE', 'BAG']

years = [73,74,75,76]
genders = ['m', 'f']
def index(request):
    
    #return render(request, 'hotornot/index.html')
    send_via_json = False
    
    if request.is_ajax and request.method == "GET":
        # get the nick name from the client side.
        gender = list(request.GET.get("gender", genders))
        collage = list(request.GET.get("collage", collages))
        faculty = list(request.GET.get("faculty", faculties))
        top_hundred = request.GET.get("top_hundred", None)
        year = list(request.GET.get("year", years))
        
        send_via_json = bool(request.GET.get("send_via_json", False))
        print(gender, collage, faculty, year)
        urls = Person.objects.using('hotornot').filter(collage__in=collage,faculty__in=faculty, year__in= year, gender__in=gender ).order_by('votes').values_list('url')[:100]
        urls = [url[0] for url in urls]
    return render(request, 'class/index.html', {'urls':urls})

'''for n,i in enumerate(Person.objects.using('hotornot').all()):
    i.year = int(i.ioe_roll_no[4:6])
    i.save()
    print(n)'''
