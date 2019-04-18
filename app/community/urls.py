from django.urls import path

from . import views

app_name = 'community'

urlpatterns = [
    path('', views.community_notice_list, name='notice'),
    path('detail/<int:community_pk>/', views.community_detail, name='detail'),
    path('comment/new/detail/<int:community_pk>/', views.comment_create, name='comment-create'),
    path('notice/create/', views.community_create, name='notice-create'),
    path('notice/delete/<int:pk>/', views.community_delete, name='community-delete'),
]
