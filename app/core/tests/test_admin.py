from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    # Setup function is a test that is run before *every* test
    def setUp(self):

        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@londenappdev.com', password='test123'
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email='test@londenappdev.com', password='test123',
            name='Test user full name'
        )

    def test_users_listed(self):
        """Test that users are listed on user page."""
        # Look at Django admin docs for more info
        url = reverse('admin:core_user_changelist')
        # Uses test client to perform HTTP GET on url
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_page_change(self):
        """Test that user edit page works."""
        # Will be something like /admin/core/user/1
        url = reverse('admin:core_user_change', args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_user_page(self):
        """Test that create user page works."""
        url = reverse('admin:core_user_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
