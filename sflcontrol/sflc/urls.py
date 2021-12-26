from genericpath import samefile
from django.conf.urls import url
from sflc import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^user$', views.user),
    url(r'^user/$', views.user),

    url(r'^user/login$', views.user),

    url(r'^user/serial$', views.user_serial),

    url(r'^account$', views.account),
    url(r'^account/$', views.account),

    url(r'^account/serial$', views.account_serial),
    
    url(r'^transaction$', views.transaction),
    url(r'^transaction/$', views.transaction),

    url(r'^vault$', views.vault),
    url(r'^vault/$', views.vault),

    url(r'^budget$', views.budget),
    url(r'^budget/$', views.budget),

    url(r'^image$', views.image),
    url(r'^image/$', views.image),
    
    url(r'^tag$', views.tag),
    url(r'^tag/$', views.tag),
]