from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^createUser$', views.create),
    url(r'^loginresult$', views.login),
    url(r'^success$', views.success),
    url(r'^jobs/new$', views.newjob),
    url(r'^createjob$', views.createprocess),
    url(r'^jobs/edit/(?P<my_id>\d+)$', views.editjob),
    url(r'^editprocess/(?P<my_id>\d+)$', views.editprocess),
    url(r'^jobs/(?P<my_id>\d+)$', views.viewprocess),
    url(r'^back$', views.back),
    url(r'^jobs/delete/(?P<my_id>\d+)$', views.remove),
    url(r'^logout$', views.logout)
]