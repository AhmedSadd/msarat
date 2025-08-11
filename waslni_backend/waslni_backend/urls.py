from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core import views as core_views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'workplaces', core_views.WorkplaceViewSet, basename='workplace')
router.register(r'drivers', core_views.DriverProfileViewSet, basename='driver')
router.register(r'vehicles', core_views.VehicleViewSet, basename='vehicle')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('admin/', admin.site.urls),

    # API routes
    path('api/', include(router.urls)),

    # Auth routes
    path('api/auth/register/', core_views.RegisterView.as_view(), name='register'),
    path('api/auth/login/', core_views.LoginView.as_view(), name='login'),

    # Profile routes
    path('api/profile/rider/', core_views.RiderProfileView.as_view(), name='rider-profile'),
]
