from django.urls import path
from .views import index, detailView, checkout
urlpatterns = [
    path('',index ,name = 'index'),
    path('<int:id>/', detailView, name= 'detail'),
    path('checkout/', checkout, name='chekout-page')
]