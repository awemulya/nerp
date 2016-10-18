from rest_framework import serializers

from hr.models import PayrollEntry, PaymentRecord, DeductionDetail, AllowanceDetail, IncentiveDetail, \
    GradeScaleValidity, EmployeeGrade, EmployeeGradeScale, EmployeeGradeGroup, AllowanceValidity, AllowanceName, \
    Allowance


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


class GradeScaleValiditySerializer(serializers.ModelSerializer):
    # TODO entry validation
    class Meta:
        model = GradeScaleValidity
        fields = '__all__'

    # def validate(self, attrs):
    #     import ipdb
    #     ipdb.set_trace()
    #     return super(GradeScaleValiditySerializer, self).validate(attrs)

    # def create(self, validated_data):
    #     import ipdb
    #     ipdb.set_trace()


class EmployeeGradeScaleSerializer(serializers.ModelSerializer):

    grade_id = serializers.ReadOnlyField(source="grade.id")
    validity_id = serializers.ReadOnlyField(source="validity.id")
    # parent_grade_id = serializers.ReadOnlyField(source="grade.group.id")
    # # parent_grade_name = serializers.ReadOnlyField(source="grade.group.name")

    class Meta:
        model = EmployeeGradeScale
        fields = (
            'id',
            'grade_id',
            'salary_scale',
            'grade_number',
            'grade_rate',
            'validity_id',

            # # Non model fields
            # 'grade_name',
            # 'parent_grade_id',
            # 'parent_grade_name'
        )


class EmployeeGradeSerializer(serializers.ModelSerializer):
    # grade_scales = EmployeeGradeScaleSerializer(many=True)
    # grade_group_id = serializers.ReadOnlyField(source="grade_group.id")
    class Meta:
        model = EmployeeGrade
        fields = ('id', 'grade_name', 'grade_group')


class EmployeeGradeGroupSerializer(serializers.ModelSerializer):
    employee_grades = EmployeeGradeSerializer(many=True)

    class Meta:
        model = EmployeeGradeGroup
        fields = ('id', 'name', 'employee_grades')


# Allowance

class AllowanceValiditySerializer(serializers.ModelSerializer):
    # TODO entry validation
    class Meta:
        model = AllowanceValidity
        fields = '__all__'

    # def validate(self, attrs):
    #     import ipdb
    #     ipdb.set_trace()
    #     return super(GradeScaleValiditySerializer, self).validate(attrs)

    # def create(self, validated_data):
    #     import ipdb
    #     ipdb.set_trace()


class AllowanceNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = AllowanceName
        fields = '__all__'


class AllowanceSerializer(serializers.ModelSerializer):
    employee_grade_id = serializers.ReadOnlyField(source='employee_grade.id')
    validity_id = serializers.ReadOnlyField(source='validity.id')
    name_id = serializers.ReadOnlyField(source='name.id')
    class Meta:
        model = Allowance
        fields = (
            'name_id',
            'employee_grade_id',
            'sum_type',
            'value',
            'payment_cycle',
            'year_payment_cycle_month',
            'validity_id'
        )

# End Allowance
