from django.urls import path

from . import views

app_name = 'product'

urlpatterns = [
    path('', views.home, name='home'),
    path('category/', views.category_list, name='category-list'),
    path('category/<int:category_pk>/', views.category_detail, name='category-detail'),
    path('category/detail/<int:product_pk>/', views.product_detail, name='product-detail'),
    path('category/cart_list/', views.my_cart, name='my-cart'),
    path('category/add_cart/<int:product_pk>/', views.add_cart, name='add-cart'),
    path('category/delete_item/<int:product_pk>/', views.my_cart_item_delete, name='delete-cart'),
    path('category/minus_cart_item/<int:product_pk>/', views.minus_cart_item, name='minus-item'),
    path('category/plus_cart_item/<int:product_pk>/', views.plus_cart_item, name='plus-item'),

    path('category/detail/comment_create/<int:product_pk>/', views.comment_create, name='comment-create'),
    path('category/detail/<int:product_pk>/comment_update/<int:pk>/', views.comment_edit, name='comment-edit'),
    path('category/detail/<int:product_id>/comment_delete/<int:comment_id>/',
         views.comment_delete, name='comment-delete'),

    path('search/', views.SearchListView.as_view(), name='search'),
]
