from rest_framework import serializers

from models import ImprestTransaction, ExpenseRow, ExpenseCategory, Expense, ImprestJournalVoucher


class ImprestTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImprestTransaction


class ExpenseRowSerializer(serializers.ModelSerializer):
    # category_id = serializers.Field()

    class Meta:
        model = ExpenseRow


class ExpenseCategorySerializer(serializers.ModelSerializer):
    url = serializers.ReadOnlyField(source='get_absolute_url')

    class Meta:
        model = ExpenseCategory


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense


class ImprestJVSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImprestJournalVoucher
