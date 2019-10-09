from django.conf.urls import url
from . import views

urlpatterns = [
    # REGISTRATION AND LOGIN
    url(r'^$', views.index),
    url(r'^books$', views.home),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^books/add$', views.addReview),
    url(r'^books/added$', views.bookAdded),
    url(r'^books/added1$', views.bookAdded1),
    url(r'^books/(?P<val>\d+)$', views.singleBookHome),
    url(r'^users/(?P<val>\d+)$', views.singleUserHome),


]