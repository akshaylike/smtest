from django.conf.urls import patterns, include, url
from transac import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^register/$', views.register, name='register'),
        url(r'^upload/$', views.upload, name='upload'),
        url(r'^viewshared/$', views.viewshared, name='viewshared'),
        url(r'^sharedoc/$', views.sharedoc, name='sharedoc'),
)
