from rest_framework import serializers
from account.models import Receipt, ReceiptRow, Account, Party


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account


class ReceiptRowSerializer(serializers.ModelSerializer):
    tax_scheme_id = serializers.Field(source='tax_scheme.id')
    budget_head_id = serializers.Field(source='budget_head.id')
    account_id = serializers.Field(source='account.id')
    activity_id = serializers.Field(source='activity.id')

    class Meta:
        model = ReceiptRow
        exclude = ['tax_scheme', 'budget_head', 'account', 'activity']


class ReceiptSerializer(serializers.ModelSerializer):
    rows = ReceiptRowSerializer(many=True)

    class Meta:
        model = Receipt


class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party