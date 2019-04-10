from django.urls import path

from . import views

app_name = 'community'

urlpatterns = [
    path('', views.community_notice_list, name='notice'),
]
