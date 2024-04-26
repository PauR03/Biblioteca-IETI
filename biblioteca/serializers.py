from rest_framework import serializers
from .models import Log

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['tipus', 'informacio', 'data', 'usuari', 'ruta']


from rest_framework import serializers
from .models import Producte

class ProducteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producte
        fields = ['titol', 'autor']