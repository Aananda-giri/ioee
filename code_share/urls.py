from django.urls import path, include
from . import views
urlpatterns = [
    #path('', views.home, name='home'),
    
    path('v0/', views.snippet_page, name='home'),
    path('<int:page>/', views.snippet_page, name="get_snippets"),
    path('code/', views.home, name='toy_post'),
    path('edit/<str:parent_id>/', views.edit_code, name='edit_code_by_parent_id'),
    path('edit/', views.edit_code, name='edit_code'), # for some strange reasons edit is sending to code/edit
    path('code/code/', views.post_detail, name='post_detail'),
    #path('<str:uuid>/', views.code_by_uuid, name='code_by_uuid'),
    path('code/<str:uuid>/', views.code_by_uuid, name='code_by_uuid'),
    path('mail/', views.sendMail, name='send_mail'),
    path('.well-known/acme-challenge/3ufveaLc9JnIgj9y5-f9jrhb8Vgz2fSAFTbKguBTMYk', views.ssl_cert, name = 'ssl_cert'),

    path('add_star/', views.add_star, name='add_star'),
    path('search', views.search_code, name='search_code'),
    path('delete', views.delete_code, name='delete_code'),

    #path('imagepage/', views.imagepage, name='imagepage'),
    path('refresh/', views.refresh, name='refresh'),

    path('', views.create_container, name = 'home2'),
    path('<int:page>/<str:is_new_container>/', views.create_container, name = 'home2'),
    path('', views.create_container, name = 'create_container'),
    path('new_container', views.new_container, name = 'new_container'),
    # path(r'(?P<page>\d+)/(?P<is_new_container>\w+)$', views.create_container, name = 'home2'),
    # path(r'(?P<page>\d+)/(?P<is_new_container>\w+)$/', views.create_container, name = 'home2'),
    path('upload/', views.upload_files, name='upload_files'),
    path('success/', views.upload_success, name='success'),
    path('containers/', views.container_list, name='container-list'),
    path('editor/', views.editor, name='editor'),
    
    path('um/', views.upload_multiple_files, name='upload_multiple_files'),
    path('uc/', views.upload_one_code, name='upload_one_code'),
    
]


from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
