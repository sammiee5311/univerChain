from django.test import TestCase

from accounts.models import MyUser, CustomAccountManager


class TestAccountsModels(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create(id=1, username='admin')
        # CustomAccountManager.create_superuser(CustomAccountManager, email='test@test.com', username='test', password='test',
        #                                       ethereum_account='test')

    def test_username(self):
        self.assertEqual(str(self.user), 'admin')
