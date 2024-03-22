from rest_framework import serializers
from .models import UnidadDeMedicion, Parametros, FactorDeConversion, CadenaDeCustodia, Mediciones

class UnidadDeMedicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadDeMedicion
        #fields=('nombre','simbolo')
        fields = '__all__'

class ParametroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametros
        fields = '__all__'

class FactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactorDeConversion
        fields = '__all__'

class CadenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CadenaDeCustodia
        fields = '__all__'

class MedicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mediciones
        fields = '__all__'
    
    def create(self, validated_data):
        unidad_de_medida = validated_data.get('unidad_de_medida')
        unidad_de_conversion = validated_data.get('unidad_de_conversion')
        parametro = validated_data.get('parametro')

        # Verificar si existe un factor de conversión para las unidades y el parámetro especificados
        try:
            factor_conversion = FactorDeConversion.objects.get(
                parametro=parametro,
                unidad_origen=unidad_de_medida,
                unidad_destino=unidad_de_conversion
            )
        except FactorDeConversion.DoesNotExist:
            raise serializers.ValidationError("No se encontró un factor de conversión para las unidades y el parámetro especificados.")

        # Si el factor de conversión existe, continuar con la creación de la medición
        return super().create(validated_data)