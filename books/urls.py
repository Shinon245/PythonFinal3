from django.conf.urls import url
from . import views

#app_name = 'pokemon'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^pokemon/$', views.book_list, name='pokemon'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^subscribe/', views.subscribe, name='subscribe'),
    url(r'^login', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^search', views.search, name='search')
]