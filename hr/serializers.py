from rest_framework import serializers

from hr.models import PayrollEntry, PaymentRecord, DeductionDetail, AllowanceDetail, IncentiveDetail


class DeductionDetailSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='deduction.name')
    editable = serializers.ReadOnlyField(source='deduction.amount_editable')

    class Meta:
        model = DeductionDetail
        fields = ('deduction', 'name', 'amount', 'editable')


class AllowanceDetailSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='allowance.name')

    class Meta:
        model = AllowanceDetail
        fields = ('allowance', 'name', 'amount')


class IncentiveDetailSerializer(serializers.ModelSerializer):
    editable = serializers.ReadOnlyField(source='incentive.amount_editable')
    name = serializers.ReadOnlyField(source='incentive.name')

    class Meta:
        model = IncentiveDetail
        fields = ('incentive', 'name', 'amount', 'editable')


class PaymentRecordSerializer(serializers.ModelSerializer):
    incentive_details = IncentiveDetailSerializer(many=True)
    allowance_details = AllowanceDetailSerializer(many=True)
    deduction_details = DeductionDetailSerializer(many=True)
    explicitly_added_row = serializers.SerializerMethodField('explicitly_added')

    employee_grade = serializers.ReadOnlyField(source='paid_employee.designation.grade.grade_name')
    employee_designation = serializers.ReadOnlyField(source='paid_employee.designation.designation_name')

    class Meta:
        model = PaymentRecord
        fields = '__all__'

    def explicitly_added(self, instance):
        return False


class PayrollEntrySerializer(serializers.ModelSerializer):
    entry_rows = PaymentRecordSerializer(many=True)

    class Meta:

        model = PayrollEntry
        fields = '__all__'
        include = ('entry_saved',)
