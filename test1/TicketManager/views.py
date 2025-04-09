from rest_framework.response import Response
from django.contrib.auth.models import User
from .serialzer import UserSerializer, TicketManagerSerializer, UserRegistrationSerializer
from .models import RoleModel, AuthUser, TicketManager
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .permission import SingleObjPermission


# Create your views here.
class UserRegistration(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class UserLogin(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = AuthUser.objects.filter(username=username).first()
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

    # def perform_create(self, serializer):
    #     serializer.save(clientId=self.request.user, role=self.request.user.role)

    def perform_create(self, serializer):
        serializer.save()


class TicketRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = TicketManager.objects.all()
    serializer_class = TicketManagerSerializer
    permission_classes = [SingleObjPermission]
