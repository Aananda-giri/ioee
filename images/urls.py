#source: https://github.com/divanov11/photo-album-app

#/person
from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    
    #path('random/', views.random_person, name='random'),
    path('', views.ImagesHome, name='images_home'),
]
