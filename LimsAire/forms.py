from django import forms
from .models import UnidadDeMedicion, Parametros, FactorDeConversion

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

class FactorForm(forms.ModelForm):
    class Meta:
        model = FactorDeConversion
        fields = ['parametro', 'unidad_origen', 'unidad_destino', 'factor']

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