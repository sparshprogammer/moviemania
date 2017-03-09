from django.conf.urls import patterns, include, url
from django.contrib import admin
from Recommendation_System import views
from django.conf import settings
from django.conf.urls.static import static# New Import
from django.core.urlresolvers import reverse



urlpatterns = patterns('',
    url(r'^$','Recommendation_System.views.index'),
    url(r'^register/$',views.register,name='register'),
    url(r'^login/$',views.user_login,name='login'),
    url(r'^restricted/?(?P<id>\d+)?/?$',views.status_update,name='status_update'),
    url(r'^rest/$',views.accept_friendship,name='accept_friendship'),
    url(r'^newsfeed/?(?P<id>\d+)?/?$',views.news_feed,name='news_feed'),
    url(r'^logout/$',views.user_logout,name='logout'),
    url(r'^profile/$',views.profile,name='profile'),
    url(r'^movies/$',views.movies,name='movies'),
    url(r'^movies/(?P<pk>[0-9]+)/$',views.DetailView.as_view(),name='detail'),
    url(r'^movies/?(?P<pk>\d+)?/?$',views.movies,name='movies'),
    url(r'^movies/add/$',views.MovieCreate.as_view(),name='movie_add'),
    url(r'^search/$',views.ajax_user_search,name='demo_user_search'),
url(r'^like/$',views.like,name='like'),
    url(r'^restrict/?(?P<id>\d+)?/?$',views.friend_request_sending,name='friend_request_sending'),

        # Examples:
    # url(r'^$', 'untitled.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
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