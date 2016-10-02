from rest_framework import serializers

from hr.models import PayrollEntry, PaymentRecord, DeductionDetail, AllowanceDetail, IncentiveDetail, \
    GradeScaleValidity, EmployeeGrade, EmployeeGradeScale


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
    is_explicitly_added_row = serializers.SerializerMethodField('explicitly_added')
    paid_employee = serializers.SerializerMethodField('get_paid_employee_as_str')

    employee_grade = serializers.ReadOnlyField(source='paid_employee.designation.grade.grade_name')
    employee_designation = serializers.ReadOnlyField(source='paid_employee.designation.designation_name')

    class Meta:
        model = PaymentRecord
        fields = '__all__'

    def explicitly_added(self, instance):
        return False

    def get_paid_employee_as_str(self, instance):
        return str(instance.paid_employee.id)


class PayrollEntrySerializer(serializers.ModelSerializer):
    entry_rows = PaymentRecordSerializer(many=True)
    edit = serializers.SerializerMethodField('get_scenario')
    branch = serializers.SerializerMethodField('get_branch_value')

    class Meta:

        model = PayrollEntry
        fields = '__all__'
        include = ('entry_saved',)

    # either edit True or False
    def get_scenario(self, instance):
        return True

    def get_branch_value(self, instance):
        if not instance.branch:
            return 'ALL'
        else:
            return instance.branch



# TODO NEst them all
class EmployeeGradeScaleValiditySerializer(serializers.ModelSerializer):

    class Meta:
        model = GradeScaleValidity
        fields = '__all__'


class EmployeeGradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeGrade
        fields = '__all__'


class EmployeeGradeScaleSerrializer(serializers.ModelSerializer):

    grade_name = serializers.ReadOnlyField(source="grade.name")
    parent_grade_id = serializers.ReadOnlyField(source="grade.group.id")
    parent_grade_name = serializers.ReadOnlyField(source="grade.group.name")

    class Meta:
        model = EmployeeGradeScale
        fields = (
            'grade',
            'salary_scale',
            'grade_number',
            'grade_rate',
            'validity',

            # Non model fields
            'grade_name',
            'parent_grade_id',
            'parent_grade_name'
        )