from rest_framework import serializers

from hr.models import PayrollEntry, PaymentRecord, DeductionDetail, AllowanceDetail, IncentiveDetail


class DeductionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeductionDetail
        fields = '__all__'


class AllowanceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllowanceDetail
        fields = '__all__'


class IncentiveDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncentiveDetail
        fields = '__all__'


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
