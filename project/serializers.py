from rest_framework import serializers

from models import ImprestTransaction, ExpenseRow, ExpenseCategory


class ImprestTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImprestTransaction

class ExpenseRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseRow

class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
