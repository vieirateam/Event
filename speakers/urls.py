from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^speaker/$', views.speakerList, name="speakerList"),
    url(r'^speaker/(?P<pk>\d+)/$', views.speakerDetail, name="speakerDetail"),
    url(r'^speaker/(?P<pk>\d+)/edit/$', views.speakerEdit, name="speakerEdit"),
 	url(r'^speaker/(?P<pk>\d+)/remove/$', views.speakerRemove, name="speakerRemove"),
 	url(r'^speaker/(?P<pk>\d+)/approve/$', views.speakerApprove, name="speakerApprove"),  
]