from django import forms
from .models import UnidadDeMedicion, Parametros, FactorDeConversion, CadenaDeCustodia, Mediciones

class UnidadForm(forms.ModelForm):
    class Meta:
        model = UnidadDeMedicion
        fields = ['nombre', 'simbolo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribir nombre de unidad'}),
            'simbolo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribir simbolo de unidad'}),
        }

class ParametroForm(forms.ModelForm):
    class Meta:
        model = Parametros
        fields = ['nombre', 'simbolo','pmolecular']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribir nombre de parametro'}),
            'simbolo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribir simbolo de parametro'}),
            'pmolecular': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escribir peso molecular en mg/mol'}),
        }

""" class FactorForm(forms.ModelForm):
    class Meta:
        model = FactorDeConversion
        fields = ['parametro', 'unidad_origen', 'unidad_destino', 'factor'] """

class FactorForm(forms.ModelForm):
    class Meta:
        model = FactorDeConversion
        fields = ['parametro', 'unidad_origen', 'unidad_destino', 'factor']
        
    def __init__(self, *args, **kwargs):
        super(FactorForm, self).__init__(*args, **kwargs)
        # Para el campo parametro
        self.fields['parametro'].queryset = Parametros.objects.all()
        # Para el campo unidad_origen
        self.fields['unidad_origen'].queryset = UnidadDeMedicion.objects.all()
        # Para el campo unidad_destino
        self.fields['unidad_destino'].queryset = UnidadDeMedicion.objects.all()


class CadenaForm(forms.ModelForm):
    class Meta:
        model = CadenaDeCustodia
        fields = [
                    'idcadena',
                    'parametro',
                    'cliente',
                    'proyecto',
                    'ciudad',
                    'muestreado_por',
                    'punto_de_muestreo',
                    'coordenada_norte',
                    'coordenada_este',
                    'altura',
                    'observaciones'
                ]
        widgets = {
            'idcadena': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribir id de cadena'}),
            'cliente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribir nombre de cliente'}),
            'proyecto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribir nombre de proyecto'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribir nombre de ciudad'}),
            'muestreado_por': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribir nombre de tecnico'}),
            'punto_de_muestreo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribir nombre de punto'}),
            'coordenada_norte': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribir coordenada norte'}),
            'coordenada_este': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribir coordenada este'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escribir altura en msm'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribir observaciones'}),
        }


class MedicionForm(forms.ModelForm):
    class Meta:
        model = Mediciones
        fields = [  
                    'cadena_custodia',
                    'parametro',
                    'fechamedicion',
                    'hora',
                    'resultado',
                    'unidad_de_medida',
                    'unidad_de_conversion',
                ]
        widgets = {
            'fechamedicion': forms.DateInput(format=('%Y-%m-%d'),attrs={'type': 'date','class': 'form-control', 'placeholder': 'Digitar fecha de medición'}),
            'hora': forms.TimeInput(format=('%H:%M'),attrs={'type': 'time','class': 'form-control', 'placeholder': 'Digitar fecha de medición'}),
        }
        

        
    def __init__(self, *args, **kwargs):
        super(MedicionForm, self).__init__(*args, **kwargs)
        self.fields['cadena_custodia'].queryset = CadenaDeCustodia.objects.all()
        self.fields['parametro'].queryset = Parametros.objects.all()
        self.fields['unidad_de_medida'].queryset = UnidadDeMedicion.objects.all()
        self.fields['unidad_de_conversion'].queryset = UnidadDeMedicion.objects.all()
        
    
    def save(self, commit=True):
        instancia = super().save(commit=False)
        try:
            factor_conversion = FactorDeConversion.objects.get(
                parametro=instancia.parametro,
                unidad_origen=instancia.unidad_de_medida,
                unidad_destino=instancia.unidad_de_conversion
            )
        except FactorDeConversion.DoesNotExist:
            raise ValueError("No se encontró un factor de conversión para los parámetros especificados.")
        else:
            # Calcular el valor de la conversión y asignarlo al campo resultado_conversion
            instancia.resultado_conversion = instancia.resultado * factor_conversion.factor

        if commit:
            instancia.save()
        return instancia

