from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^index.html', views.index),
    # url(r'^test', views.test),
    url(r'^suggest.html', views.suggest),
    url(r'^drawpicture', views.drawpicture)
]