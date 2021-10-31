from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='register'),
    path('attend/<str:username>/', views.fuse_attend, name='attend_by_user'),

]
