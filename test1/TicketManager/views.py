from rest_framework.response import Response
from django.contrib.auth.models import User
from .serialzer import UserSerializer, TicketManagerSerializer
from .models import RoleModel, AuthUser, TicketManager
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .permission import SingleObjPermission


# Create your views here.

class UserLogin(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            refresh['role'] = user.role.name

            return Response(
                {'refresh': str(refresh),
                 'access': str(refresh.access_token)
                 })

        return Response({'error': 'Invalid User'}, status=status.HTTP_400_BAD_REQUEST)


class TicketList(ListCreateAPIView):
    queryset = TicketManager.objects.all()
    serializer_class = TicketManagerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(clientId=self.request.user, role=self.request.user.role)


class TicketRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = TicketManager.objects.all()
    serializer_class = TicketManagerSerializer
    permission_classes = [SingleObjPermission]
