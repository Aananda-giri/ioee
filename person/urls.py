from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('search/', views.search, name='search_me'),
    path('profile/', views.profile, name='profile'),
    path('add_people/', views.add_people, name='add_people'),
    path('updateprofile/', views.update_profile, name='updateprofile'),
]
