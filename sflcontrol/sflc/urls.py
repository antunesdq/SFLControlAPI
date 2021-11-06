from genericpath import samefile
from django.conf.urls import url
from sflc import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^user$', views.user),
    url(r'^users/$', views.user),
    url(r'^login$', views.login),
]