from django.conf.urls import url, include
from django.conf.urls.static import static
from mysite import settings
from django.contrib import admin
from django.contrib.auth import views
from events import views as events_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/logout/$', views.logout, name='logout', kwargs={'next_page': '/'}),
    url(r'^register/$', events_views.register, name="register"), 
    url(r'', include('events.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)