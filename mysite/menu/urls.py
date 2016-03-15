from django.conf.urls import url
from . import views
#Created by Django, slightly modified by us

#Valid url patterns to direct and render
app_name = "menu"
urlpatterns = [
	url(r'^$', views.get_travel_info, name= 'index'),
	url(r'^results/$', views.return_directions, name='thanks')
	]