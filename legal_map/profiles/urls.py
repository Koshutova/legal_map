from django.urls import path
from django.conf.urls import url
from legal_map.profiles import views
urlpatterns = (
    path('', views.profile_details, name='profile details'),
    url(r'^password/$', views.change_password, name='change_password'),
)