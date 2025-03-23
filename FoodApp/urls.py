from django.urls import path
from . import views

app_name = 'Foodapp'
urlpatterns = [
    path('',views.index, name= 'index'),
    path('<int:pk>/', views.details, name='details'),
    #Add Items
    path('add/', views.create_item, name ='create_item'),
    # Edit item
    path('update/<int:pk>/', views.update_item, name='edit_item'),
    # delete Item
    path('delete/<int:pk>/', views.delete_item, name='delete_item')
]