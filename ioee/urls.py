"""ioee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from hotornot import views as hotornot_views
#from code_share.views import ssl_cert
from api import views as api

from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('hotornot', include('hotornot.urls')),
    path('fuse/', hotornot_views.fuse_attend, name='fuse_attend'),
    path('fusee/', hotornot_views.fuse_attendd, name='fuse_attend2'),
    path('fuse', include('fuse_attend.urls')),
    path('class/', include('class.urls')),
    path('api/', include('api.urls')),
    path('', include('code_share.urls')),
    path('code/', include('code_share.urls')),
    path('people/', include('person.urls')),
    #path('.well-known/acme-challenge/M58vqliMosBAdgOYNx9UW9DlcBQ71UIkaQ0YYWAq_zs', ssl_cert, name = ssl_cert)
    
    
    
    
    # for login and logout
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
#=======
#>>>>>>> c11fb71da6e85de028a4900d352127ffa232e1f4
]
