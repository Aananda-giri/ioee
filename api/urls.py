from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_new_notifications, name='notifications')
    path('<int:how_many>/', views.get_saved_notifications, name='saved_notifications')
]
