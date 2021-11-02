from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_new_notifications, name='notifications')
]
