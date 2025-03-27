from django.urls import path
from .views import UserLogin, TicketList, TicketRetrieveUpdateDestroy

urlpatterns = [
    path('login/', UserLogin.as_view, name='login'),
    path('ticket/add/', TicketList.as_view(), name='thicket-add'),
    path('ticket/list/', TicketList.as_view(), name='thicket-list'),
    path('ticket/update/<int:pk>', TicketRetrieveUpdateDestroy.as_view(), name='ticket-update'),
    path('ticket/delete/<int:pk>', TicketRetrieveUpdateDestroy.as_view(), name='ticket-delete')
]
