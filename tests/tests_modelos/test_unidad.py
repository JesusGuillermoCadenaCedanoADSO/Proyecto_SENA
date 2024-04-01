
from django.test import TestCase
from django.contrib.auth.models import User
from LimsAire.models import UnidadDeMedicion



class test_UnidadDeMedicion(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        usuario = User.objects.create_user(username='jesuscadena', password='123')
        UnidadDeMedicion.objects.create(user=usuario,nombre='partes por mil', simbolo='ppt')
    
    
    def test_nombre(self):
        unidad=UnidadDeMedicion.objects.get(id=1)
        field_label = unidad._meta.get_field('nombre').verbose_name
        self.assertEqual(field_label,'nombre')
    
    def test_simbolo(self):
        unidad=UnidadDeMedicion.objects.get(id=1)
        field_label = unidad._meta.get_field('simbolo').verbose_name
        self.assertEqual(field_label,'simbolo')

    def test_simbolo_max_length(self):
        unidad=UnidadDeMedicion.objects.get(id=1)
        max_length = unidad._meta.get_field('simbolo').max_length
        self.assertEqual(max_length,45)
    
    def test_representacion_unidad(self):
        unidad=UnidadDeMedicion.objects.get(id=1)
        expected_object_name = unidad.nombre + " "+"(" + unidad.simbolo + ")"
        self.assertEqual(expected_object_name,str(unidad))

    def test_get_absolute_url(self):
        unidad=UnidadDeMedicion.objects.get(id=1)
        #Esto también fallará si la urlconf no está definida.
        self.assertEqual(unidad.get_absolute_url(),'/listar_unidades/1/')


class TestUnidadDeMedicion(TestCase):
    
    def setUp(self):
        self.usuario = User.objects.create_user(username='jesuscadena', password='123')
        self.unidad = UnidadDeMedicion.objects.create(user=self.usuario, nombre='partes por mil', simbolo='ppt')

    def test_creacion_unidad(self):
        self.assertEqual(UnidadDeMedicion.objects.count(), 1)
        # self.assertEqual(self.unidad.nombre, 'partes por mil')

    def test_edicion_unidad(self):
        self.unidad.nombre = 'PPT'
        self.unidad.save()
        self.unidad.refresh_from_db()
        self.assertEqual(self.unidad.nombre, 'PPT')

    def test_eliminacion_unidad(self):
        self.unidad.delete()
        with self.assertRaises(UnidadDeMedicion.DoesNotExist):
            UnidadDeMedicion.objects.get(id=self.unidad.id)

    
