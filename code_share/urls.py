from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.toy_post, name='toy_post'),
    path('code/', views.post_detail, name='post_detail'),
    path('<str:uuid>/', views.code_by_uuid, name='code_by_uuid'),
    path('mail/', views.sendMail, name='send_mail'),
]

