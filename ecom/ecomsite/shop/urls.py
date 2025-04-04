from django.urls import path
from .views import index, detailView
urlpatterns = [
    path('',index ,name = 'index'),
    path('<int:id>/', detailView, name= 'detail')
]