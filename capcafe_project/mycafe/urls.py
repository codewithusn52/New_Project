from django.urls import path
from . import views
app_name = 'mycafe'

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu_list, name='menu_list'),
    path('item/<int:pk>/', views.MenuItemDetailView.as_view(), name='item_detail'), # Dynamic URL parameter
    path('item/add/', views.item_create, name='item_create'),
    path('item/<int:pk>/edit/', views.item_update, name='item_update'),
    path('item/<int:pk>/delete/', views.item_delete, name='item_delete'),
]
