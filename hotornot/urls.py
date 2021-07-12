from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('gender_only/', views.gender_only, name='gender_only'),
    path('gender/<str:gender>/', views.gender_details, name='gender'),
    path('', views.collage_faculty_details, name='collage'),
    path('vote_image/', views.vote, name='vote_image'),
    path('polls/', views.polls, name='polls'),
    path('test/', views.test, name='test'),
    #path('index/', views.index, name='index'),
    #path('search/', views.search, name='search_me'),
    #path('profile/', views.profile, name='profile'),
    #path('add_people/', views.add_people, name='add_people'),
    
    path('feedback/', views.feedback, name='feedback'),
    
]
