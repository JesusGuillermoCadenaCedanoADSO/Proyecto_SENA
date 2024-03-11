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
    idunidad=models.UUIDField(primary_key=True,default=uuid.uuid4,help_text='identificador de unidad de medicion')
    nombre = models.CharField(max_length=45)
    simbolo = models.CharField(max_length=45)
    fecha_generacion = models.DateField()
    nombre_encargado = models.CharField(max_length=45)
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
    unidad_origen = models.ForeignKey(UnidadDeMedicion, related_name='unidad_origen', default=1, on_delete=models.RESTRICT)
    unidad_destino = models.ForeignKey(UnidadDeMedicion, related_name='unidad_destino', default=1, on_delete=models.RESTRICT)
    factor = models.FloatField()
    fechacreacion = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=45)


    def __str__(self):
        return self.parametros + ' de ' + self.unidadorigen + ' a ' + self.unidaddestino

    def get_absolute_url(self):
        return reverse('factor-conversion-detail', args=[str(self.id)])


class CadenaDeCustodia(models.Model):
    idcadena = models.CharField('PM',
        max_length=20,
        unique=True,
        help_text="Identificador de cadena de custodia)"
    )
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
    user = models.CharField(max_length=45)

    def __str__(self):
        return self.idcadena + ' de proyecto ' + self.proyecto

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields='idcadena',
                name='CadenaDeCustodia_idcadena_case_sensitive_unique'
            ),
        ]

    def get_absolute_url(self):
        return reverse('cadena-de-custodia-detail', args=[str(self.id)])


class AsignacionesDeParametros(models.Model):
    parametros = models.ForeignKey(Parametros, on_delete=models.RESTRICT)
    cadena_de_custodia = models.ForeignKey(CadenaDeCustodia, on_delete=models.RESTRICT)
    fechacreacion = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=45)

    def __str__(self):
        return self.parametros + ' de cadena ' + self.cadena_de_custodia


class Mediciones(models.Model):
    asignaciones_parametros = models.ForeignKey(AsignacionesDeParametros, on_delete=models.RESTRICT)
    fechamedicion = models.DateField(null=False, blank=False)
    hora = models.TimeField(null=False, blank=False)
    resultado = models.FloatField(default=0)
    unidad_de_medida = models.CharField(max_length=45)
    unidad_de_conversion = models.CharField(max_length=45)
    resultado_conversion = models.FloatField(default=0)
    fechacreacion = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=45)

    def __str__(self):
        return self.fechamedicion + ' de asignacion ' + self.asignaciones_parametros

    def get_absolute_url(self):
        return reverse('cadena-de-custodia-detail', args=[str(self.id)])



