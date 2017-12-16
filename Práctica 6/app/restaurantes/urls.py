from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^test_template/$', views.test_template, name='test_template'),
  url(r'^create/$', views.create_restaurant, name='create_restaurant'),
  url(r'^edit/$', views.edit_restaurant, name='edit_restaurant'),
  url(r'^find/$', views.find_restaurant_view, name='find_restaurant_view'),
  url(r'^find/(cuisine|name|borough|zip)', views.find_restaurant, name='find_restaurant'),
  url(r'^find/detail/(?P<id>[0-9]+)', views.restaurant_detail_view, name='detail_restaurant'),
  url(r'^stadistics/$', views.stadistics_view, name='stadistics'),
  url(r'^stadistics/get/$', views.stadistics, name='stadistics_ajax'),
  url(r'^password/$', views.change_password, name='change_password'),
]
