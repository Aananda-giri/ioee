#/person
from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('random/', views.random_person, name='random'),
    path('search/', views.search, name='search_me'),
    path('ioe_student/<str:ioe_roll_no>/', views.ioe_search, name='ioe_search'),
    path('uid/<str:uid>/', views.uid_search, name='uid_search'),
    path('profile/', views.profile, name='profile'),
    path('add_people/', views.add_people, name='add_people'),
    path('updateprofile/', views.update_profile, name='updateprofile'),
    
    path('ioe_images/<str:collage>/<str:faculty>/<str:year_code>/', views.get_ioe_photos, name='ioe_images'),
    path('save_image_url/',views.save_image_url,name = 'save_image_url'),
    path('flush/', views.flush, name = 'flush'),
    path('.well-known/acme-challenge/M58vqliMosBAdgOYNx9UW9DlcBQ71UIkaQ0YYWAq_zs', views.ssl_cert, name = 'ssl_cert'),

    path('verify/<str:ioe_roll_no>/<str:last_name>/<str:dob_bs>/', views.verify, name = 'verify'),
]
