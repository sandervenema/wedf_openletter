from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sign/$', views.sign, name='sign'),
    url(r'^confirm/([0-9a-z]{64})/$', views.confirm, name='confirm'),
]
