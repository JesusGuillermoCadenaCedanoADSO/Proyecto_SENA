import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from LimsAire.models import Parametros
from django.db import IntegrityError



class ParametrosTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Creamos un usuario para asociarlo a los parámetros
        cls.user = User.objects.create_user(username='test_user', password='test_password')

    def test_simbolo_unique_constraint(self):
        # Creamos dos parámetros con el mismo símbolo
        Parametros.objects.create(nombre='Parametro 1', simbolo='sym', pmolecular=10, user=self.user)
        with self.assertRaises(IntegrityError):
            Parametros.objects.create(nombre='Parametro 2', simbolo='sym', pmolecular=20, user=self.user)

    def is_number(self,s):
            try:
                float(s)
                return True
            except ValueError:
                return False

    def test_pmolecular_numeric_type(self):
        
       
        # Creamos un parámetro con pmolecular como número flotante
        Parametros.objects.create(nombre='Parametro 2', simbolo='sym2', pmolecular=15.5, user=self.user)

        # Verificamos que el pmolecular es numérico
        parametro = Parametros.objects.get(simbolo='sym2')
        # self.assertIsInstance(parametro.pmolecular, float)
        self.assertTrue(ParametrosTestCase().is_number(parametro.pmolecular))

    
    def test_pmolecular_nonumeric_type(self):

        
        # Creamos un parámetro con pmolecular como string
        with self.assertRaises(ValueError):
            Parametros.objects.create(nombre='Parametro 1', simbolo='sym1', pmolecular='not_numeric', user=self.user)



""" class test_Parametros(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        usuario = User.objects.create_user(username='jesuscadena', password='123')
        Parametros.objects.create(user=usuario,nombre='Amonio', simbolo='NH4', pmolecular=18)
    
    
    def test_nombre(self):
        Parametro=Parametros.objects.get(id=1)
        field_label = Parametro._meta.get_field('nombre').verbose_name
        self.assertEqual(field_label,'nombre')
    
    def test_simbolo(self):
        Parametro=Parametros.objects.get(id=1)
        field_label = Parametro._meta.get_field('simbolo').verbose_name
        self.assertEqual(field_label,'simbolo')

    def test_simbolo_max_length(self):
        Parametro=Parametros.objects.get(id=1)
        max_length = Parametro._meta.get_field('simbolo').max_length
        self.assertEqual(max_length,10)
    
    def test_representacion_parametro(self):
        Parametro=Parametros.objects.get(id=1)
        expected_object_name = Parametro.nombre
        self.assertEqual(expected_object_name,str(Parametro))

    def test_get_absolute_url(self):
        Parametro=Parametros.objects.get(id=1)
        #Esto también fallará si la urlconf no está definida.
        self.assertEqual(Parametro.get_absolute_url(),'/listar_parametros/1/')

     """

""" class TestParametros(TestCase):
    
    def setUp(self):
        self.usuario = User.objects.create_user(username='jesuscadena', password='123')
        self.Parametro = Parametros.objects.create(user=self.usuario, nombre='Amonio', simbolo='NH4', pmolecular=18)

    def test_creacion_Parametro(self):
        self.assertEqual(self.Parametro.nombre, 'Amonio')

    def test_edicion_Parametro(self):
        self.Parametro.nombre = 'AMONIO'
        self.Parametro.save()
        self.Parametro.refresh_from_db()
        self.assertEqual(self.Parametro.nombre, 'AMONIO')

    def test_eliminacion_Parametro(self):
        self.Parametro.delete()
        with self.assertRaises(Parametros.DoesNotExist):
            Parametros.objects.get(id=self.Parametro.id) """

    