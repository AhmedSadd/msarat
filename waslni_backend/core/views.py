from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from .serializers import UserSerializer, WorkplaceSerializer, RiderProfileSerializer, DriverProfileSerializer, VehicleSerializer
from .models import Workplace, RiderProfile, DriverProfile, Vehicle

class DriverProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for admins to manage driver profiles.
    """
    queryset = DriverProfile.objects.all()
    serializer_class = DriverProfileSerializer
    permission_classes = [permissions.IsAdminUser]

class VehicleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for admins to manage vehicles.
    """
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAdminUser]

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    Read-only access is allowed for any authenticated user.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        # Write permissions are only allowed to admin users
        return request.user and request.user.is_staff


class WorkplaceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows workplaces to be viewed or edited.
    """
    queryset = Workplace.objects.all()
    serializer_class = WorkplaceSerializer
    permission_classes = [IsAdminOrReadOnly]


class RiderProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for the current user to retrieve and update their Rider Profile.
    """
    serializer_class = RiderProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # It's possible the user is a driver and doesn't have a rider profile.
        # We create one if it doesn't exist.
        profile, created = RiderProfile.objects.get_or_create(user=self.request.user)
        return profile


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        })

# The login view will be the default ObtainAuthToken view from DRF
LoginView = ObtainAuthToken
