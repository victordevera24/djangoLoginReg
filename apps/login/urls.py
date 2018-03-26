from django.conf.urls import url
from . import views          
  
urlpatterns = [
    url(r'^$', views.index),
    url(r'process$', views.process),   
    url(r'dashboard$', views.success), 
    url(r'login$', views.login),
    url(r'add$', views.add),
    url(r'addItem$', views.addItem),
    url(r'item/(?P<id>\d+)$', views.show),
    url(r'addWish/(?P<id>\d+)$', views.addWish),
    url(r'remove/(?P<id>\d+)$', views.remove),
    url(r'delete/(?P<id>\d+)$', views.delete),

]