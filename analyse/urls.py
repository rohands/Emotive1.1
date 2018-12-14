from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^send_sms/$', views.send_sms, name='send_sms'),
    url(r'^receive_sms/$', views.receive_sms, name='receive_sms')
]