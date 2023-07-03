from django.urls import path, include
from . import views
urlpatterns = [
    #path('', views.home, name='home'),
    path('', views.snippet_page, name='home'),
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
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)










"""
# filter code whose title is 'test' and body is 'test'
Code.objects.filter(title='test')
Code.objects.filter(title__contains='test', code__contains='test')


# filter code whose title and body are same
from django.db.models import F
Code.objects.filter(title__exact=models.F('code')).delete()

# delete code whose body is null or empty string
from code_share.models import Code
from django.db.models import Q

Code.objects.filter(Q(code__isnull=True) | Q(code__exact='')).delete()

"""