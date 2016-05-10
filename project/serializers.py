from rest_framework import serializers

from models import ImprestTransaction, ExpenseRow


class ImprestTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImprestTransaction

class ExpenseRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseRow
