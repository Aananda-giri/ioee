from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='toy_post'),
    path('code/', views.home, name='toy_post'),
    path('edit/<str:parent_id>/', views.edit_code, name='edit_code'),
    path('edit/', views.edit_code, name='edit_code'),
    path('code/code/', views.post_detail, name='post_detail'),
    #path('<str:uuid>/', views.code_by_uuid, name='code_by_uuid'),
    path('codee/<str:uuid>/', views.code_by_uuid, name='code_by_uuid'),
    path('mail/', views.sendMail, name='send_mail'),
    path('.well-known/acme-challenge/3ufveaLc9JnIgj9y5-f9jrhb8Vgz2fSAFTbKguBTMYk', views.ssl_cert, name = 'ssl_cert'),

    path('add_star/', views.add_star, name='add_star'),
]
