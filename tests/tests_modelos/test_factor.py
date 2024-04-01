import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from LimsAire.models import Parametros, UnidadDeMedicion, FactorDeConversion
from django.db import transaction
from django.db import IntegrityError

class FactorDeConversionTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Creamos un usuario para asociarlo a las instancias
        cls.user = User.objects.create_user(username='test_user', password='test_password')

    
    def test_parametro_faltante(self):

        # Creamos una instancia de UnidadDeMedicion
        unidad_origen = UnidadDeMedicion.objects.create(nombre='Unidad de Origen', simbolo='sym_origen', user=self.user)
        unidad_destino = UnidadDeMedicion.objects.create(nombre='Unidad de Destino', simbolo='sym_destino', user=self.user)

        # Intentamos crear una instancia de FactorDeConversion sin proporcionar parametro
        with self.assertRaises(IntegrityError):
            FactorDeConversion.objects.create(unidad_origen=unidad_origen, unidad_destino=unidad_destino, factor=1, user=self.user)

    def test_parametro_None(self):

        # Creamos una instancia de UnidadDeMedicion
        unidad_origen = UnidadDeMedicion.objects.create(nombre='Unidad de Origen', simbolo='sym_origen', user=self.user)
        unidad_destino = UnidadDeMedicion.objects.create(nombre='Unidad de Destino', simbolo='sym_destino', user=self.user)

        # Intentamos crear una instancia de FactorDeConversion con parametro como None
        with self.assertRaises(IntegrityError):
            FactorDeConversion.objects.create(parametro=None, unidad_origen=unidad_origen, unidad_destino=unidad_destino, factor=1, user=self.user)

    def test_parametro_invalido(self):
       
        # Creamos una instancia de UnidadDeMedicion
        unidad_origen = UnidadDeMedicion.objects.create(nombre='Unidad de Origen', simbolo='sym_origen', user=self.user)
        unidad_destino = UnidadDeMedicion.objects.create(nombre='Unidad de Destino', simbolo='sym_destino', user=self.user)

        # Intentamos crear una instancia de FactorDeConversion con parametro como una instancia no válida de Parametros
        with self.assertRaises(ValueError):
            FactorDeConversion.objects.create(parametro='invalid_parametro', unidad_origen=unidad_origen, unidad_destino=unidad_destino, factor=1, user=self.user)

    def test_parametro_valido(self):
        # Creamos una instancia de Parametros
        parametro = Parametros.objects.create(nombre='Parametro 1', simbolo='sym1', pmolecular=10, user=self.user)

        # Creamos una instancia de UnidadDeMedicion
        unidad_origen = UnidadDeMedicion.objects.create(nombre='Unidad de Origen', simbolo='sym_origen', user=self.user)
        unidad_destino = UnidadDeMedicion.objects.create(nombre='Unidad de Destino', simbolo='sym_destino', user=self.user)


        # Creamos una instancia de FactorDeConversion con parametro válido
        factor_conversion = FactorDeConversion.objects.create(parametro=parametro, unidad_origen=unidad_origen, unidad_destino=unidad_destino, factor=1, user=self.user)

        # Verificamos que se haya creado correctamente
        self.assertEqual(factor_conversion.parametro, parametro)