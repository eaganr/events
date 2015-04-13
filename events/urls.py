from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from events import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^event/(?P<hashtag>\w+)/$', views.event, name='event'),
    url(r'^vote/$', views.vote, name='vote'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social.apps.django_app.urls', namespace='social'))

)
