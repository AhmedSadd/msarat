from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

from .models import Workplace, DriverProfile

class WorkplaceAPITest(APITestCase):
    """
    Test suite for the Workplace API.
    """
    def setUp(self):
        # Create a regular user (rider)
        self.user = User.objects.create_user(username='rider', password='password123')

        # Create an admin user
        self.admin_user = User.objects.create_superuser(username='admin', password='password123', email='admin@example.com')

        # Create a workplace instance to be used in tests
        self.workplace = Workplace.objects.create(name='Test Corp', address='123 Test St', latitude=1.0, longitude=1.0)

    def test_list_workplaces_authenticated(self):
        """Ensure any authenticated user can list workplaces."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('workplace-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_workplaces_unauthenticated(self):
        """Ensure unauthenticated users cannot list workplaces."""
        response = self.client.get(reverse('workplace-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_workplace_as_admin(self):
        """Ensure admin can create a workplace."""
        self.client.force_authenticate(user=self.admin_user)
        data = {'name': 'NewCo', 'address': '456 New Ave', 'latitude': 2.0, 'longitude': 2.0}
        response = self.client.post(reverse('workplace-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workplace.objects.count(), 2)

    def test_create_workplace_as_regular_user(self):
        """Ensure regular user cannot create a workplace."""
        self.client.force_authenticate(user=self.user)
        data = {'name': 'NewCo', 'address': '456 New Ave', 'latitude': 2.0, 'longitude': 2.0}
        response = self.client.post(reverse('workplace-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Workplace.objects.count(), 1)


from .models import RiderProfile

class RiderProfileAPITest(APITestCase):
    """
    Test suite for the Rider Profile API.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='rider', password='password123')
        self.workplace = Workplace.objects.create(name='Test Corp', address='123 Test St', latitude=1.0, longitude=1.0)
        # The view now creates the profile on-the-fly, so we don't need to create it here.
        # self.profile = RiderProfile.objects.create(user=self.user, home_address='555 Home St')

    def test_get_profile_authenticated(self):
        """Ensure authenticated user can retrieve their profile."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('rider-profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that a default profile was created
        self.assertEqual(response.data['home_address'], '')

    def test_get_profile_unauthenticated(self):
        """Ensure unauthenticated user cannot retrieve a profile."""
        response = self.client.get(reverse('rider-profile'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_profile_authenticated(self):
        """Ensure authenticated user can update their profile."""
        self.client.force_authenticate(user=self.user)
        data = {
            'home_address': '987 New Home Lane',
            'home_latitude': 3.0,
            'home_longitude': 4.0,
            'workplace': self.workplace.id
        }
        response = self.client.put(reverse('rider-profile'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['home_address'], '987 New Home Lane')

        # Verify the change in the database
        profile = RiderProfile.objects.get(user=self.user)
        self.assertEqual(profile.home_address, '987 New Home Lane')
        self.assertEqual(profile.workplace.id, self.workplace.id)


class DriverAPITest(APITestCase):
    """
    Test suite for the Driver API.
    """
    def setUp(self):
        self.regular_user = User.objects.create_user(username='rider', password='password123')
        self.admin_user = User.objects.create_superuser(username='admin', password='password123')

    def test_list_drivers_as_admin(self):
        """Ensure admin can list drivers."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('driver-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_drivers_as_regular_user(self):
        """Ensure regular user cannot list drivers."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(reverse('driver-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_driver_as_admin(self):
        """Ensure admin can create a new driver user and profile."""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "username": "newdriver",
            "email": "driver@example.com",
            "password": "password123"
        }
        response = self.client.post(reverse('driver-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newdriver").exists())
        self.assertTrue(DriverProfile.objects.filter(user__username="newdriver").exists())


from .models import Vehicle

class VehicleAPITest(APITestCase):
    """
    Test suite for the Vehicle API.
    """
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='password123')
        driver_user = User.objects.create_user(username='driver', password='password123')
        self.driver_profile = DriverProfile.objects.create(user=driver_user)

    def test_create_vehicle_as_admin(self):
        """Ensure admin can create a vehicle."""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "vehicle_type": "Van",
            "capacity": 8,
            "license_plate": "TEST-123",
            "driver": self.driver_profile.id
        }
        response = self.client.post(reverse('vehicle-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vehicle.objects.count(), 1)
        self.assertEqual(Vehicle.objects.get().license_plate, "TEST-123")


class RegistrationAPITest(APITestCase):
    """
    Test suite for the user registration API endpoint.
    """

    def test_register_user_success(self):
        """
        Ensure we can create a new user and a token is returned.
        """
        url = reverse('register') # We named this in our core.urls
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'somepassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post(url, data, format='json')

        # Check for a successful response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the user was created in the database
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

        # Check that the response contains user data and a token
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']['username'], 'testuser')

    def test_register_user_missing_fields(self):
        """
        Ensure registration fails if required fields are missing.
        """
        url = reverse('register')
        data = {
            'username': 'testuser2',
            # Missing password and email
        }

        response = self.client.post(url, data, format='json')

        # Check for a bad request response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that no user was created
        self.assertEqual(User.objects.count(), 0)
