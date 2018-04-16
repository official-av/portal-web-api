from django.conf.urls import url
from .views import *
from . import views


urlpatterns = [

    # url(r'^$',home,name="home"),

    #url(r'^login/$',login,name="login"),
    url(r'^process_order/$',views.process_order , name='process_order'),
    url(r'^send_pin/$',views.ajax_send_pin,name='ajax_send_pin'),

]
