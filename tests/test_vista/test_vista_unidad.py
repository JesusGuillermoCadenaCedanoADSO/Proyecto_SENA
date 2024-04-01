from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from rest_framework.test import APIClient
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory


from LimsAire.models import UnidadDeMedicion
from LimsAire.views import listar_unidades

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission 



class UnidadListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        
        cls.factory = APIRequestFactory()
        cls.client = APIClient()
        numero_unidades = 5
        usuario = User.objects.create_user(username='jesuscadena', password='123',is_active=True)
        
        for i in range(numero_unidades):
            UnidadDeMedicion.objects.create(user=usuario,nombre='unidad_' + str(i), simbolo='un_'+str(i))
        
    def test_view_url_exists_at_desired_location(self):
        
        
        request = self.factory.get('/listar_unidades/')
        view=listar_unidades
        force_authenticate(request, user=User.objects.get(username='jesuscadena'))

        response = view(request)

        self.assertEqual(response.status_code, 200)
        
    def test_view_url_accessible_by_name(self):
        request = self.factory.get(reverse('listar_unidades'))
        view=listar_unidades
        force_authenticate(request, user=User.objects.get(username='jesuscadena'))
        response = view(request)
        self.assertEqual(response.status_code, 200)

""" 
    def test_view_uses_correct_json_content(self):
        request = self.factory.get(reverse('listar_unidades'))
        view=listar_unidades
        force_authenticate(request, user=User.objects.get(username='jesuscadena'))
        response = view(request)
        response.render()
        print(response.content.decode('utf-8'))
        self.assertContains(response,'"id":1')
        self.assertContains(response,'"nombre":"unidad_0"')
        self.assertContains(response,'"simbolo":"un_0"')
        self.assertContains(response,'"user":1')
        
    def test_view_uses_correct_template(self):
        request = self.factory.get(reverse('listar_unidades'), HTTP_ACCEPT='text/html')
        view=listar_unidades
        force_authenticate(request, user=User.objects.get(username='jesuscadena'))
        response = view(request)
        # print(response.content.decode('utf-8')) 
        self.assertContains(response,'<!DOCTYPE html>', html=True)
        self.assertContains(response,'Listado de unidades de medición', html=True)
        self.assertContains(response,'id de unidad', html=True)
        self.assertContains(response,'nombre de unidad', html=True)
        self.assertContains(response,'símbolo de unidad', html=True)
        self.assertContains(response,'<td><a href="/listar_unidades/1/">unidad_0</a></td>', html=True)
 """        


""" #prueba fallida
User = get_user_model()
class prueba(TestCase):
    def setUp(self):
        # Create two users
        self.test_user1 = User.objects.create_user(username='jcc', password='123')
        permission = Permission.objects.get(name='Set book as returned')
        # self.test_user1.save()
        self.test_user1.user_permissions.add(permission)
        self.test_user1.save()
        self.unidad = UnidadDeMedicion.objects.create(user=self.test_user1,nombre='unidad_0' , simbolo='un_0')

    def test_view_url_exists_at_desired_location(self):
        response=self.client.force_login(User.objects.get(username='jcc'))
        response = self.client.get('/listar_unidades/')
        self.assertEqual(response.status_code, 200)

 """