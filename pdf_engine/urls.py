from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.search, name='pdf_search'),
]


from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
