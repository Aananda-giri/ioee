from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('code/', views.home, name='toy_post'),
    path('edit/<str:parent_id>/', views.edit_code,
         name='edit_code_by_parent_id'),
    # for some strange reasons edit is sending to code/edit
    path('edit/', views.edit_code, name='edit_code'),
    path('code/code/', views.post_detail, name='post_detail'),
    #path('<str:uuid>/', views.code_by_uuid, name='code_by_uuid'),
    path('code/<str:uuid>/', views.code_by_uuid, name='code_by_uuid'),
    path('mail/', views.sendMail, name='send_mail'),
    path('.well-known/acme-challenge/3ufveaLc9JnIgj9y5-f9jrhb8Vgz2fSAFTbKguBTMYk',
         views.ssl_cert, name='ssl_cert'),

    path('add_star/', views.add_star, name='add_star'),
    path('search', views.search_code, name='search_code'),
    path('delete', views.delete_code, name='delete_code'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
