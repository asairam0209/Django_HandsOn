from django.urls import path
from .views import UserLogin, TicketList, TicketRetrieveUpdateDestroy, UserRegistration

urlpatterns = [
    path('login/', UserLogin.as_view(), name='login'),
    path('register/', UserRegistration.as_view(), name = 'registration'),
    path('ticket/add/', TicketList.as_view(), name='ticket-add'),
    path('ticket/list/', TicketList.as_view(), name='ticket-list'),
    path('ticket/update/<int:pk>', TicketRetrieveUpdateDestroy.as_view(), name='ticket-update'),
    path('ticket/delete/<int:pk>', TicketRetrieveUpdateDestroy.as_view(), name='ticket-delete')
]
