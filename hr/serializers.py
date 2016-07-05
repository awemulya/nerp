from rest_framework import serializers

from hr.models import PayrollEntry, PaymentRecord, DeductionDetail, AllowanceDetail, IncentiveDetail


class DeductionDetailSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='deduction.name')
    class Meta:
        model = DeductionDetail
        fields = ('deduction', 'name', 'amount')


class AllowanceDetailSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='allowance.name')
    class Meta:
        model = AllowanceDetail
        fields = ('allowance', 'name', 'amount')


class IncentiveDetailSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='incentive.name')
    class Meta:
        model = IncentiveDetail
        fields = ('incentive', 'name', 'amount')


class PaymentRecordSerializer(serializers.ModelSerializer):
    incentive_details = IncentiveDetailSerializer(many=True)
    allowance_details = AllowanceDetailSerializer(many=True)
    deduction_details = DeductionDetailSerializer(many=True)
    class Meta:
        model = PaymentRecord
        fields = '__all__'

class PayrollEntrySerializer(serializers.ModelSerializer):
    entry_rows = PaymentRecordSerializer(many=True)
    class Meta:
        model = PayrollEntry
        fields = '__all__'
