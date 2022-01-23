from django.urls import path

from . import views

urlpatterns = [
    
    path('<int:how_many>/', views.get_saved_notifications, name='saved_notifications'),
    
    #to implement/improve
    #path('new/', views.NotiList.as_view()),
    #path('new/<int:pk>/', views.NotiDetail.as_view()),
    
    path('', views.new_notifications_view, name='notifications'),#scraps new notifications (i.e. first 1 page and compare to previously stored)
]
