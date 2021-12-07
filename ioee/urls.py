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
from tiktok import views as toktok_views
#<<<<<<< HEAD
from api import views as api
#=======
#>>>>>>> c11fb71da6e85de028a4900d352127ffa232e1f4

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('hotornot', include('hotornot.urls')),
    path('fuse/', hotornot_views.fuse_attend, name='fuse_attend'),
    path('fusee/', hotornot_views.fuse_attendd, name='fuse_attend2'),
    path('fuse', include('fuse_attend.urls')),
    path('class/', include('class.urls')),
    path('tiktok_s_v_web_id/', toktok_views.get_tiktok_s_v_web_id, name='get_tiktok_s_v_web_id'),
#<<<<<<< HEAD
    path('api/', include('api.urls')),
    path('', include('code_share.urls')),
    path('code/', include('code_share.urls')),
#=======
#>>>>>>> c11fb71da6e85de028a4900d352127ffa232e1f4
]
