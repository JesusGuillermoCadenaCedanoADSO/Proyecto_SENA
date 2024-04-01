from django.test import TestCase
from django.contrib.auth.models import User
from LimsAire.forms import MedicionForm
from LimsAire.models import UnidadDeMedicion, Parametros, FactorDeConversion, CadenaDeCustodia
from datetime import date, time, datetime

class TestMedicionForm(TestCase):
    def setUp(self):
        # Crear instancia de usuario
        self.user = User.objects.create(id='100',username='testuser')

        # Crear instancias de modelos necesarios para la prueba
        self.unidad_medida = UnidadDeMedicion.objects.create(nombre='Unidad de medida', simbolo='UM', user=self.user)
        self.unidad_conversion = UnidadDeMedicion.objects.create(nombre='Unidad de conversión', simbolo='UC', user=self.user)
        self.parametro = Parametros.objects.create(nombre='Parámetro', simbolo='P', pmolecular=1.0, user=self.user)
        self.cadena_custodia = CadenaDeCustodia.objects.create(
            idcadena='1', cliente='Cliente', proyecto='Proyecto', ciudad='Ciudad',
            muestreado_por='Técnico', punto_de_muestreo='Punto', coordenada_norte='Norte',
            coordenada_este='Este', altura=1.0, observaciones='Observaciones', user=self.user
        )

        # Crear instancia de FactorDeConversion
        self.factor_conversion = FactorDeConversion.objects.create(
            parametro=self.parametro,
            unidad_origen=self.unidad_medida,
            unidad_destino=self.unidad_conversion,
            factor=2.0,
            user=self.user
        )

        # Crear instancia de formulario con datos para la prueba
        self.data = {
            'user':1,
            'cadena_custodia': self.cadena_custodia.id,
            'parametro': self.parametro.id,
            'fechamedicion': '2023-03-18',
            'hora': '12:00:00',
            'resultado': 10.0,
            'unidad_de_medida': self.unidad_medida.id,
            'unidad_de_conversion': self.unidad_conversion.id
        }
        self.form = MedicionForm(data=self.data)

    def test_save_method(self):
        #return True
        # Guardar el formulario y asegurarse de que no se lance ninguna excepción
        self.form.instance.user = self.user
        self.form.is_valid()
        self.form.save()
        
        # Obtener la instancia de Mediciones creada
        medicion = self.form.instance

        # Verificar que el resultado de la conversión se haya calculado correctamente
        resultado_conversion_esperado = self.data['resultado'] * self.factor_conversion.factor
        self.assertEqual(medicion.resultado_conversion, resultado_conversion_esperado)

        # También puedes agregar otras aserciones según tus necesidades
        # Por ejemplo, puedes verificar que los valores de los campos se hayan guardado correctamente en la instancia
        self.assertEqual(medicion.cadena_custodia.id, self.cadena_custodia.id)
        self.assertEqual(medicion.parametro.id, self.parametro.id)
        fecha_cadena = '2023-03-18'
        fecha_objeto = datetime.strptime(fecha_cadena, '%Y-%m-%d').date()
        self.assertEqual(medicion.fechamedicion, fecha_objeto )
        hora_cadena='12:00'
        hora_objeto = datetime.strptime(hora_cadena, '%H:%M').time()
        self.assertEqual(medicion.hora, hora_objeto)
        self.assertEqual(medicion.resultado, 10.0)
        self.assertEqual(medicion.unidad_de_medida.id, self.unidad_medida.id)
        self.assertEqual(medicion.unidad_de_conversion.id, self.unidad_conversion.id)


