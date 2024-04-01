from django.test import Client
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class Tests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(Tests, cls).setUpClass()

        # a command for create a superuser for a testing
        call_command('factory_test_superusers', '1')

        cls.active_superuser = get_user_model().objects.get()

    def setUp(self):
        c = Client()
        c.force_login(self.active_superuser)

    def test_1(self):
        pass

    def test_2(self):
        pass