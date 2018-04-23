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
    url(r'^talk/(?P<pk>\d+)/$', views.talkDetail, name="talkDetail"),
    url(r'^talk/new/$', views.talkNew, name="talkNew"),
    url(r'^talk/(?P<pk>\d+)/edit/$', views.talkEdit, name="talkEdit"),
    url(r'^talk/(?P<pk>\d+)/remove/$', views.talkRemove, name="talkRemove"),
    url(r'^talk/(?P<pk>\d+)/approve/$', views.talkApprove, name="talkApprove"),
]