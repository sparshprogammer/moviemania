from django.conf.urls import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = patterns('',

               )
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
if not settings.DEBUG:
        urlpatterns += static(
            settings.STATIC_URL, document_root=settings.STATIC_ROOT)