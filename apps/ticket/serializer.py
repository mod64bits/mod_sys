from rest_framework import serializers
from .models import IamagemAtendimento


class UploadImagemAtendimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IamagemAtendimento
        fields = '__all__'

