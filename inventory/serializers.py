from rest_framework import serializers
from inventory.models import Demand, DemandRow, Item, Party, PurchaseOrder, PurchaseOrderRow, HandoverRow, Handover, \
    EntryReport, EntryReportRow, JournalEntry, InspectionRow, Inspection, Transaction, ItemLocation, Depreciation, \
    ItemInstance, \
    Release


class ItemInstanceSerializer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField()

    class Meta:
        model = ItemInstance
        exclude = ['other_properties']

    def get_properties(self, obj):
        return obj.other_properties


class ItemLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemLocation


class DepreciationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depreciation


class ItemSerializer(serializers.ModelSerializer):
    account_no = serializers.ReadOnlyField(source='account.account_no')
    depreciation = DepreciationSerializer()

    class Meta:
        model = Item
        exclude = ['depreciation']


class ReleaseSerializer(serializers.ModelSerializer):
    item_instance = ItemInstanceSerializer()

    class Meta:
        model = Release


class DemandRowSerializer(serializers.ModelSerializer):
    item_id = serializers.ReadOnlyField(source='item.id')
    releases = ReleaseSerializer(many=True)

    class Meta:
        model = DemandRow
        exclude = ['item']


class DemandSerializer(serializers.ModelSerializer):
    # rows = serializers.PrimaryKeyRelatedField(
    #     queryset=DemandRow.objects.all(),
    #     many=True)
    rows = DemandRowSerializer(many=True)
    date = serializers.DateField(format=None)

    class Meta:
        model = Demand


class PurchaseOrderRowSerializer(serializers.ModelSerializer):
    item_id = serializers.ReadOnlyField(source='item.id')

    class Meta:
        model = PurchaseOrderRow


class PurchaseOrderSerializer(serializers.ModelSerializer):
    rows = PurchaseOrderRowSerializer(many=True)
    date = serializers.DateField(format=None)

    class Meta:
        model = PurchaseOrder


class HandoverRowSerializer(serializers.ModelSerializer):
    item_id = serializers.ReadOnlyField(source='item.id')

    class Meta:
        model = HandoverRow


class HandoverSerializer(serializers.ModelSerializer):
    rows = HandoverRowSerializer(many=True)
    date = serializers.DateField(format=None)

    class Meta:
        model = Handover


class EntryReportRowSerializer(serializers.ModelSerializer):
    item_id = serializers.ReadOnlyField(source='item.id')

    class Meta:
        model = EntryReportRow
        exclude = ['item']


class EntryReportSerializer(serializers.ModelSerializer):
    rows = EntryReportRowSerializer(many=True)

    class Meta:
        model = EntryReport


class InventoryAccountRowSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='id')
    voucher_no = serializers.ReadOnlyField(source='creator.get_voucher_no')
    specification = serializers.ReadOnlyField(source='creator.specification')
    country_or_company = serializers.SerializerMethodField('get_country_or_company')
    size = serializers.SerializerMethodField('get_size')
    expected_life = serializers.SerializerMethodField('get_expected_life')
    source = serializers.SerializerMethodField('get_source')
    income_quantity = serializers.SerializerMethodField('get_income_quantity')
    income_rate = serializers.SerializerMethodField('get_income_rate')
    income_total = serializers.SerializerMethodField('get_income_total')
    expense_quantity = serializers.SerializerMethodField('get_expense_quantity')
    expense_total_cost_price = serializers.SerializerMethodField('get_expense_total_cost_price')
    remaining_total_cost_price = serializers.SerializerMethodField('get_remaining_total_cost_price')
    remarks = serializers.SerializerMethodField('get_remarks')
    current_balance = serializers.SerializerMethodField('get_current_balance')
    date = serializers.DateField(format=None)

    class Meta:
        model = JournalEntry

    def get_country_or_company(self, obj):
        try:
            return obj.account_row.country_of_production_or_company_name
        except:
            return ''

    def get_size(self, obj):
        try:
            return obj.account_row.size
        except:
            return ''

    def get_expected_life(self, obj):
        try:
            return obj.account_row.expected_life
        except:
            return ''

    def get_source(self, obj):
        try:
            return obj.account_row.source
        except:
            return ''

    def get_income_quantity(self, obj):
        if obj.creator.__class__ == DemandRow:
            return ''
        return obj.creator.quantity

    def get_income_rate(self, obj):
        if obj.creator.__class__ == DemandRow:
            return ''
        return obj.creator.rate

    def get_income_total(self, obj):
        if obj.creator.__class__ == DemandRow:
            return ''
        import math

        return math.ceil(obj.creator.total_entry_cost() * 100) / 100

    def get_expense_quantity(self, obj):
        if obj.creator.__class__ == EntryReportRow:
            return ''
        return obj.creator.release_quantity

    def get_expense_total_cost_price(self, obj):
        try:
            return obj.account_row.expense_total_cost_price or ''
        except:
            return ''

    def get_remaining_total_cost_price(self, obj):
        try:
            return obj.account_row.remaining_total_cost_price or ''
        except:
            return ''

    def get_remarks(self, obj):
        try:
            return obj.account_row.remarks
        except:
            return ''

    def get_current_balance(self, obj):
        return obj.transactions.filter(account=obj.creator.item.account)[0].current_balance


class InspectionRowSerializer(serializers.ModelSerializer):
    item_name = serializers.ReadOnlyField(source="transaction.account.item.name")
    item_account_number = serializers.ReadOnlyField(source="transaction.account.account_no")
    item_property_classification_reference_number = serializers.ReadOnlyField(
        source="transaction.account.item.property_classification_reference_number")
    item_unit = serializers.ReadOnlyField(source="transaction.account.item.unit")
    item_quantity = serializers.ReadOnlyField(source="transaction.dr_amount")

    class Meta:
        model = InspectionRow
        exclude = ['transaction']


class InspectionSerializer(serializers.ModelSerializer):
    rows = InspectionRowSerializer(many=True)

    class Meta:
        model = Inspection


class TransactionSerializer(serializers.ModelSerializer):
    account_no = serializers.ReadOnlyField(source="account.account_no")
    current_balance = serializers.ReadOnlyField(source="account.current_balance")
    inventory_classification_reference_no = serializers.ReadOnlyField(
        source="account.item.property_classification_reference_number")
    item_name = serializers.ReadOnlyField(source="account.item.name")
    unit = serializers.ReadOnlyField(source="account.item.unit")
    rate = serializers.ReadOnlyField(source="journal_entry.creator.rate")
    total_dr_amount = serializers.ReadOnlyField()
    total_dr_amount_without_rate = serializers.ReadOnlyField()
    depreciation = DepreciationSerializer(source="account.item.depreciation")

    class Meta:
        model = Transaction
        exclude = ['dr_amount', 'cr_amount', 'current_balance', 'account', 'journal_entry']
