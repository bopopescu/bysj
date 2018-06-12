from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.adminlogin),
    url(r'^adminindex',views.adminindex),
    # url(r'^test', views.getWordCloud)
    url(r'^getIindustryTrend',views.getIindustryTrend)
]