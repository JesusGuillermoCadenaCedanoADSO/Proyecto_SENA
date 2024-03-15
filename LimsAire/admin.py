from django.contrib import admin
from .models import Parametros, UnidadDeMedicion, FactorDeConversion, CadenaDeCustodia,  \
    Mediciones

admin.site.register(Parametros)
admin.site.register(UnidadDeMedicion)
admin.site.register(FactorDeConversion)
admin.site.register(CadenaDeCustodia)
admin.site.register(Mediciones)


# Register your models here.
