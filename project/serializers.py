from rest_framework import serializers

from models import ImprestTransaction, ExpenseRow, ExpenseCategory, Expense, BudgetAllocationItem


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


class BudgetAllocationItemSerializer(serializers.ModelSerializer):
    budget_head_id = serializers.ReadOnlyField(source='budget_head.id')
    aid_name = serializers.SerializerMethodField()

    class Meta:
        model = BudgetAllocationItem
        exclude = ('budget_head', 'aid',)

    def get_aid_name(self, obj):
        name = None
        if obj.aid:
            name = str(obj.aid.id) + '-' + obj.aid.donor.name
        return name
