from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^register', views.register, name='register'),
    url(r'^$', views.my_login, name='my_login'),
    url(r'^logout', views.my_logout, name='my_logout'),
]