from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^pendency/$', views.pendencyList, name="pendencyList"),
    url(r'^event/$', views.eventList, name="eventList"),
    url(r'^event/(?P<pk>\d+)/$', views.eventDetail, name="eventDetail"),
    url(r'^event/new/$', views.eventNew, name="eventNew"),
    url(r'^event/(?P<pk>\d+)/edit/$', views.eventEdit, name="eventEdit"),
    url(r'^event/(?P<pk>\d+)/remove/$', views.eventRemove, name="eventRemove"),
    url(r'^speaker/$', views.speakerList, name="speakerList"),
    url(r'^speaker/(?P<pk>\d+)/$', views.speakerDetail, name="speakerDetail"),
    url(r'^speaker/(?P<pk>\d+)/edit/$', views.speakerEdit, name="speakerEdit"),
    url(r'^speaker/(?P<pk>\d+)/remove/$', views.speakerRemove, name="speakerRemove"),
    url(r'^speaker/(?P<pk>\d+)/approve/$', views.speakerApprove, name="speakerApprove"),  
    url(r'^talk/(?P<pk>\d+)/$', views.talkDetail, name="talkDetail"),
    url(r'^talk/new/$', views.talkNew, name="talkNew"),
    url(r'^talk/(?P<pk>\d+)/edit/$', views.talkEdit, name="talkEdit"),
    url(r'^talk/(?P<pk>\d+)/remove/$', views.talkRemove, name="talkRemove"),
    url(r'^talk/(?P<pk>\d+)/approve/$', views.talkApprove, name="talkApprove"),
    url(r'^events/$', views.eventListJson, name="eventListJson"),
    url(r'^events/(?P<pk>\d+)/$', views.eventDetailJson, name="eventDetailJson"),
    url(r'^speakers/$', views.speakerListJson, name="speakerListJson"),
    url(r'^speakers/(?P<pk>\d+)/$', views.speakerDetailJson, name="speakerDetailJson"),
    url(r'^talks/(?P<pk>\d+)/$', views.talkDetailJson, name="talkDetailJson"),
]