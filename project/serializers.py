from rest_framework import serializers

from models import ImprestTransaction


class ImprestTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImprestTransaction
