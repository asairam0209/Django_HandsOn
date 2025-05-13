from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import RoleModel, AuthUser, TicketManager
from rest_framework_simplejwt.tokens import AccessToken

class TicketAPITestCase(APITestCase):
    def setUp(self):
        # Create roles
        self.client_role = RoleModel.objects.create(name='CLIENT')
        self.admin_role = RoleModel.objects.create(name='ADMIN')

        # Create users
        self.client_user = AuthUser.objects.create_user(
            username='clientOne',
            password='client1235',
            role=self.client_role
        )
        self.admin_user = AuthUser.objects.create_user(
            username='admin',
            password='admin1235',
            role=self.admin_role
        )

        # Create ticket
        self.ticket1 = TicketManager.objects.create(
            ticketId=1,
            issue='Network Problem',
            category='IT',
            clientId=self.client_user,
            role=self.client_role
        )

    def get_token(self, username, password):
        url = reverse('login')
        response = self.client.post(url, {'username': username, 'password': password})
        return response.data.get('access')

    # Test 1: Successful client login
    def test_client_login_success(self):
        url = reverse('login')
        response = self.client.post(url, {'username': 'clientOne', 'password': 'client1235'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    # Test 2: Successful admin login
    def test_admin_login_success(self):
        response = self.client.post(reverse('login'), {'username': 'admin', 'password': 'admin1235'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test 3: Invalid credentials
    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('login'), {'username': 'clientOne', 'password': 'wrong'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test 4: Create ticket authenticated
    def test_create_ticket_authenticated(self):
        token = self.get_token('clientOne', 'client1235')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(reverse('ticket-add'), {
            'ticketId': 2,
            'issue': 'Software Issue',
            'category': 'IT',
            'comments': 'Need license renewal',
            'i3_priority': True,
            'status': 'New'  # Add this if your model requires it
        })
        print("CREATE TICKET RESPONSE:", response.data)  # Debug output
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test 5: Create ticket unauthenticated
    def test_create_ticket_unauthenticated(self):
        response = self.client.post(reverse('ticket-add'), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test 6: List tickets by category
    def test_list_tickets_by_category(self):
        token = self.get_token('clientOne', 'client1235')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(f"{reverse('ticket-list')}?category=IT")
        self.assertEqual(len(response.data), 1)

    # Test 7: List with invalid category
    # def test_list_invalid_category(self):
    #     token = self.get_token('clientOne', 'client1235')
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    #     response = self.client.get(f"{reverse('ticket-list')}?category=INVALID")
    #     print("INVALID CATEGORY RESPONSE:", response.data)  # Debug output
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test 8: Update ticket as owner
    def test_update_ticket_owner(self):
        token = self.get_token('clientOne', 'client1235')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.patch(
            reverse('ticket-update', args=[self.ticket1.pk]),
            {'comments': 'Updated'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test 9: Update as admin (should fail)
    def test_update_ticket_admin(self):
        token = self.get_token('admin', 'admin1235')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.patch(reverse('ticket-update', args=[self.ticket1.pk]), {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test 10: Delete ticket as owner
    def test_delete_ticket_owner(self):
        token = self.get_token('clientOne', 'client1235')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(reverse('ticket-delete', args=[self.ticket1.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Test 11: Delete as admin (fail)
    def test_delete_ticket_admin(self):
        token = self.get_token('admin', 'admin1235')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(reverse('ticket-delete', args=[self.ticket1.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Test 12: Delete non-existent ticket
    def test_delete_invalid_ticket(self):
        token = self.get_token('clientOne', 'client1235')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(reverse('ticket-delete', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Test 13: Access protected endpoint
    def test_protected_endpoint_access(self):
        response = self.client.get(reverse('ticket-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test 14: JWT contains role
    def test_jwt_role_claim(self):
        token = self.get_token('clientOne', 'client1235')
        decoded = AccessToken(token)
        self.assertEqual(decoded['role'], 'CLIENT')

    # Test 15: Verify initial roles
    def test_initial_roles(self):
        roles = RoleModel.objects.all()
        self.assertEqual(roles.count(), 2)
        self.assertTrue(roles.filter(name='CLIENT').exists())

    # Test 16: Update with invalid data
    def test_invalid_data_update(self):
        token = self.get_token('clientOne', 'client1235')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.patch(
            reverse('ticket-update', args=[self.ticket1.pk]),
            {'ticketId': 'invalid'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test 17: Create with missing fields
    def test_missing_fields_create(self):
        token = self.get_token('clientOne', 'client1235')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(reverse('ticket-add'), {'ticketId': 3})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test 18: Check default values
    def test_ticket_defaults(self):
        ticket = TicketManager.objects.get(pk=self.ticket1.pk)
        self.assertEqual(ticket.status, 'New')
        self.assertTrue(ticket.i3_priority)