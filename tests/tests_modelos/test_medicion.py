from django.test import TestCase
from django.contrib.auth.models import User
from LimsAire.models import Mediciones, CadenaDeCustodia, Parametros, UnidadDeMedicion, FactorDeConversion
from datetime import date, time
from django.core.exceptions import ValidationError

class MedicionesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Creamos un usuario para asociarlo a las mediciones
        cls.user = User.objects.create_user(username='test_user', password='test_password')

        # Creamos instancias necesarias para las mediciones
        cls.cadena_custodia = CadenaDeCustodia.objects.create(
            idcadena='ID123',
            cliente='Cliente',
            proyecto='Proyecto',
            ciudad='Ciudad',
            muestreado_por='Muestreador',
            punto_de_muestreo='Punto de muestreo',
            coordenada_norte='12346',
            coordenada_este='45687',
            altura=10.5,
            observaciones='Observaciones',
            user=cls.user
        )

        cls.parametro = Parametros.objects.create(
            nombre='parametro',
            simbolo='SMB',
            pmolecular=10.0,
            user=cls.user
        )

        cls.unidad_medida = UnidadDeMedicion.objects.create(
            nombre='Unidad de medida',
            simbolo='UM',
            user=cls.user
        )

        cls.unidad_conversion = UnidadDeMedicion.objects.create(
            nombre='Unidad de conversión',
            simbolo='UC',
            user=cls.user
        )

        cls.factor_conversion = FactorDeConversion.objects.create(
            parametro=cls.parametro,
            unidad_origen=cls.unidad_medida,
            unidad_destino=cls.unidad_conversion,
            factor=2.0,
            user=cls.user
        )

    def test_tipo_fechamedicion_fecha(self):
        medicion = Mediciones.objects.create(
            cadena_custodia=self.cadena_custodia,
            parametro=self.parametro,
            fechamedicion=date.today(),
            hora=time(12, 0),
            resultado=10.0,
            unidad_de_medida=self.unidad_medida,
            unidad_de_conversion=self.unidad_conversion,
            user=self.user
        )
        self.assertIsInstance(medicion.fechamedicion, date)

    def test_tipo_fechamedicion_NoFecha(self):
        with self.assertRaises(ValidationError):
            Mediciones.objects.create(
                cadena_custodia=self.cadena_custodia,
                parametro=self.parametro,
                fechamedicion='no_fecha',
                hora=time(12, 0),
                resultado=10.0,
                unidad_de_medida=self.unidad_medida,
                unidad_de_conversion=self.unidad_conversion,
                user=self.user
            )
        

    def test_tipo_hora(self):
        medicion = Mediciones.objects.create(
            cadena_custodia=self.cadena_custodia,
            parametro=self.parametro,
            fechamedicion=date.today(),
            hora=time(12, 0),
            resultado=10.0,
            unidad_de_medida=self.unidad_medida,
            unidad_de_conversion=self.unidad_conversion,
            user=self.user
        )
        self.assertIsInstance(medicion.hora, time)
    
    def test_tipo_no_hora(self):
        with self.assertRaises(ValidationError):
            Mediciones.objects.create(
                cadena_custodia=self.cadena_custodia,
                parametro=self.parametro,
                fechamedicion=date.today(),
                hora='',
                resultado=10.0,
                unidad_de_medida=self.unidad_medida,
                unidad_de_conversion=self.unidad_conversion,
                user=self.user
            )
        

    def test_obtener_factor_conversion(self):
        medicion = Mediciones.objects.create(
            cadena_custodia=self.cadena_custodia,
            parametro=self.parametro,
            fechamedicion=date.today(),
            hora=time(12, 0),
            resultado=10.0,
            unidad_de_medida=self.unidad_medida,
            unidad_de_conversion=self.unidad_conversion,
            user=self.user
        )
        # Verificamos que el resultado de la conversión sea 20.0, ya que el factor de conversión es 2.0
        self.assertEqual(medicion.resultado_conversion, 20)

    def test_obtener_factor_conversion_caso_fallido(self):

        with self.assertRaises(ValueError):
            Mediciones.objects.create(
                cadena_custodia=self.cadena_custodia,
                parametro=self.parametro,
                fechamedicion=date.today(),
                hora=time(12, 0),
                resultado=10.0,
                unidad_de_medida=self.unidad_medida,
                unidad_de_conversion='unidad_conversion',
                user=self.user
            )

