from django.db import models

# Create your models here.
from django.urls import reverse # Used in get_absolute_url() to get URL for specified ID
import uuid

from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field
from django.contrib.auth.models import User


class Parametros(models.Model):
    """Este modelo representa a un parámetro"""
    nombre = models.CharField(max_length=200)
    simbolo = models.CharField(max_length=10, unique=True)
    pmolecular = models.FloatField(null=False, blank=False)
    fechacreacion = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # ManyToManyField usado por que  una unidad puede estar relacionada con varios parametros
    # un parametro puede estar relacionado con varias unidades


    def __str__(self):
        """cadena que representa al parámetro."""
        return self.nombre

    def get_absolute_url(self):
        """retorna la url del parametro."""
        return reverse('parametro-detail', args=[str(self.id)])



class UnidadDeMedicion(models.Model):
    idunidad = models.UUIDField(primary_key=True,default=uuid.uuid4,help_text='identificador de unidad de medicion')
    nombre = models.CharField(max_length=45)
    simbolo = models.CharField(max_length=45)
    # fecha_generacion = models.DateField()
    fechacreacion = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """cadena que representa al parámetro."""
        return self.nombre + " simbolo : " + self.simbolo

    def get_absolute_url(self):
        """retorna la url del parametro."""
        return reverse('unidad-detail', args=[str(self.id)])



class FactorDeConversion(models.Model):
    parametros = models.ForeignKey(Parametros, on_delete=models.RESTRICT)
    # unidadorigen = models.SmallIntegerField()
    # unidaddestino = models.SmallIntegerField()
    unidad_origen = models.ForeignKey(UnidadDeMedicion, related_name='unidad_origen', default=1,
                                      on_delete=models.RESTRICT)
    unidad_destino = models.ForeignKey(UnidadDeMedicion, related_name='unidad_destino', default=1,
                                       on_delete=models.RESTRICT)
    factor = models.FloatField(default=1)
    fechacreacion = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.parametros.nombre + ' de ' + self.unidad_origen.simbolo + ' a ' + self.unidad_destino.simbolo

    def get_absolute_url(self):
        return reverse('factor-conversion-detail', args=[str(self.id)])


class CadenaDeCustodia(models.Model):
    idcadena = models.CharField('PM',
        max_length=20,
        help_text="Identificador de cadena de custodia)"
    )
    parametro = models.ManyToManyField(Parametros, help_text='Seleccionar parámetro')
    cliente = models.CharField(max_length=45)
    proyecto = models.CharField(max_length=45)
    ciudad = models.CharField(max_length=45)
    muestreado_por = models.CharField(max_length=45)
    punto_de_muestreo = models.CharField(max_length=45)
    coordenada_norte = models.CharField(max_length=45)
    coordenada_este = models.CharField(max_length=45)
    altura = models.FloatField()
    observaciones = models.TextField(
        max_length=1000, help_text="Ingrese una breve descripción de la toma de muestras")
    fechacreacion = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.idcadena + ' de proyecto ' + self.proyecto


    def get_absolute_url(self):
        return reverse('cadena-de-custodia-detail', args=[str(self.id)])


# class AsignacionesDeParametros(models.Model):
#     parametros = models.ForeignKey(Parametros, on_delete=models.RESTRICT)
#     cadena_de_custodia = models.ForeignKey(CadenaDeCustodia, on_delete=models.RESTRICT)
#     fechacreacion = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.parametros.nombre + ' de cadena ' + self.cadena_de_custodia.idcadena


class Mediciones(models.Model):
    # asignaciones_parametros = models.ForeignKey(AsignacionesDeParametros, on_delete=models.RESTRICT)
    # cadena_custodia = models.ManyToManyField(CadenaDeCustodia, help_text='Seleccionar cadena de custodia')

    cadena_custodia = models.ForeignKey(CadenaDeCustodia, default=1, on_delete=models.RESTRICT,
                                        help_text='Seleccionar cadena de custodia')
    parametro = models.ForeignKey(Parametros, default=1, on_delete=models.RESTRICT, help_text='Seleccionar parametro')

    fechamedicion = models.DateField(null=False, blank=False)
    hora = models.TimeField(null=False, blank=False)
    resultado = models.FloatField(default=0)
    unidad_de_medida = models.ForeignKey(UnidadDeMedicion, related_name='unidad_de_medicion', default=1,
                                         on_delete=models.RESTRICT)
    unidad_de_conversion = models.ForeignKey(UnidadDeMedicion, related_name='unidad_de_conversion', default=1,
                                             on_delete=models.RESTRICT)
    resultado_conversion = models.FloatField(default=1,editable=False)
    fechacreacion = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Asignar por defecto el valor de resultado al resultado_conversion
    #     self.resultado_conversion = models.FloatField(default=self.resultado)
    #     print('valor por defecto: ', str(self.resultado_conversion))

    def save(self, *args, **kwargs):
        # Consultar el factor de conversión
        try:
            factor_conversion = FactorDeConversion.objects.get(
                parametros=self.parametro,
                unidad_origen=self.unidad_de_medida,
                unidad_destino=self.unidad_de_conversion
            )
        except FactorDeConversion.DoesNotExist:
            # self.resultado_conversion = self.resultado
            # self.unidad_de_conversion = self.unidad_de_medida
            raise ValueError("No se encontró un factor de conversión para los parámetros especificados.")
        else:
        # Calcular el resultado de la conversión
            self.resultado_conversion = self.resultado * factor_conversion.factor
        finally:
            super().save(*args, **kwargs)
            print('valor ingresado: ', self.resultado)
            print('valor calculado: ',self.resultado_conversion)


    def __str__(self):
        # return "medicion de " + self.asignaciones_parametros.parametros.nombre + \
        #        '   de plan ' + self.asignaciones_parametros.cadena_de_custodia.idcadena + \
        #        ' tomada el dia ' + str(self.fechamedicion) + ' a las ' + str(self.hora) \
        #        + ' por ' + self.user.username
        return "medicion de " + \
         '  plan ' + self.cadena_custodia.idcadena + \
            ' de parametro ' + self.parametro.nombre + \
                ' tomada el dia ' + str(self.fechamedicion) + ' a las ' + str(self.hora) \
               + ' por ' + self.user.username

    def get_absolute_url(self):
        return reverse('cadena-de-custodia-detail', args=[str(self.id)])



