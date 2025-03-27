from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import RoleModel, AuthUser, TicketManager
from django.contrib.auth.hashers import make_password


class TicketAPITestCase(APITestCase):
    def setUp(self):
        # Create roles
        self.client_role = RoleModel.objects.create(name='CLIENT')
        self.admin_role = RoleModel.objects.create(name='ADMIN')

        # Create users
        self.client_user = AuthUser.objects.create_user(
            username='clientOne',
            password='client1235',
            email='client1@gmail.com',
            role=self.client_role
        )
        self.admin_user = AuthUser.objects.create_user(
            username='admin',
            password='admin1235',
            email='admin@gmail.com',
            role=self.admin_role
        )

        # Create tickets
        self.ticket1 = TicketManager.objects.create(
            ticketId=1,
            issue='Network Problem',
            category='IT',
            i3_priority=True,
            comments='Urgent fix needed',
            clientId=self.client_user,
            role=self.client_role
        )

    # Helper method to get JWT token
    def get_token(self, username, password):
        url = reverse('login')

        response = self.client.post(url, {'username': username, 'password': password})
        return response.data.get('access')

    # Test Case 1: Successful client login
    def test_client_login_success(self):
        url = reverse('login')
        data = {'username': 'clientOne', 'password': 'client1235'}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    # Test Case 2: Successful admin login
    def test_admin_login_success(self):
        url = reverse('login')
        data = {'username': 'admin', 'password': 'admin1235'}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test Case 3: Login with invalid credentials
    def test_login_invalid_credentials(self):
        url = reverse('login')
        data = {'username': 'clientOne', 'password': 'wrongpass'}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test Case 4: Add ticket as authenticated client
    def test_create_ticket_authenticated_client(self):
        token = self.get_token('clientOne', 'client1235')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('ticket-add')
        data = {
            'ticketId': 2,
            'issue': 'Software Issue',
            'category': 'IT',
            'comments': 'Need license renewal'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test Case 5: Add ticket without authentication
    def test_create_ticket_unauthenticated(self):
        url = reverse('ticket-add')

        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test Case 6: List tickets by category
    def test_list_tickets_by_category(self):
        token = self.get_token('clientOne', 'client1235')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('ticket-list') + '?category=IT'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)

    # Test Case 7: List tickets with invalid category
    def test_list_tickets_invalid_category(self):
        token = self.get_token('clientOne', 'client1235')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('ticket-list') + '?category=INVALID'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test Case 8: Update ticket as owner
    def test_update_ticket_owner(self):
        token = self.get_token('clientOne', 'client1235')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('ticket-update', args=[self.ticket1.pk])
        data = {'comments': 'Updated comment'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test Case 9: Update ticket as admin (should fail)
    def test_update_ticket_admin(self):
        token = self.get_token('admin', 'admin1235')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('ticket-update', args=[self.ticket1.pk])
        response = self.client.patch(url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test Case 10: Delete ticket as owner
    def test_delete_ticket_owner(self):
        token = self.get_token('clientOne', 'client1235')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('ticket-delete', args=[self.ticket1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Test Case 11: Delete ticket as admin (should fail)
    def test_delete_ticket_admin(self):
        token = self.get_token('admin', 'admin1235')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('ticket-delete', args=[self.ticket1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test Case 12: Delete non-existent ticket
    def test_delete_nonexistent_ticket(self):
        token = self.get_token('clientOne', 'client1235')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('ticket-delete', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Test Case 13: Access protected endpoint without token

    def test_protected_endpoint_without_token(self):
        url = reverse('ticket-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test Case 14: JWT contains role information

    def test_jwt_contains_role(self):
        token = self.get_token('clientOne', 'client1235')
        self.assertIsNotNone(token)
        self.assertIn('role', token)

        # Test Case 15: Initial role setup

    def test_initial_roles_exist(self):
        roles = RoleModel.objects.all()
        self.assertEqual(roles.count(), 2)
        self.assertTrue(roles.filter(name='CLIENT').exists())
        self.assertTrue(roles.filter(name='ADMIN').exists())

        # Test Case 16: Update ticket with invalid data

    def test_update_ticket_invalid_data(self):
        token = self.get_token('clientOne', 'client1235')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('ticket-update', args=[self.ticket1.pk])
        data = {'ticketId': 'invalid'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test Case 17: Create ticket with missing required fields
    def test_create_ticket_missing_fields(self):
        token = self.get_token('clientOne', 'client1235')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('ticket-add')
        data = {'ticketId': 3}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test Case 18: List all tickets
    def test_list_all_tickets(self):
        token = self.get_token('admin', 'admin1235')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('ticket-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test Case 19: Client access admin-only endpoint

    def test_client_access_admin_endpoint(self):
        token = self.get_token('clientOne', 'client1235')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('admin-endpoint')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Test Case 20: Check ticket default values

    def test_ticket_default_values(self):
        ticket = TicketManager.objects.get(pk=self.ticket1.pk)

        self.assertEqual(ticket.status, 'New')
        self.assertEqual(ticket.i3_priority, True)
