from rest_framework import serializers
from .models import CoverLetter, ProcessedCoverLetter


class CoverLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverLetter
        fields = '__all__'


class ProcessedCoverLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedCoverLetter
        fields = '__all__'
