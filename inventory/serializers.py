from rest_framework import serializers
from inventory.models import Demand, DemandRow, Item, Party, PurchaseOrder, PurchaseOrderRow, HandoverRow, Handover, EntryReport, EntryReportRow, JournalEntry


class ItemSerializer(serializers.ModelSerializer):
    account_no = serializers.ReadOnlyField(source='account.account_no')

    class Meta:
        model = Item


class DemandRowSerializer(serializers.ModelSerializer):
    item_id = serializers.ReadOnlyField(source='item.id')

    class Meta:
        model = DemandRow
        exclude = ['item']


class DemandSerializer(serializers.ModelSerializer):
    rows = DemandRowSerializer(many=True)
    date = serializers.DateField(format=None)

    class Meta:
        model = Demand


class PurchaseOrderRowSerializer(serializers.ModelSerializer):
    item_id = serializers.Field(source='item.id')

    class Meta:
        model = PurchaseOrderRow


class PurchaseOrderSerializer(serializers.ModelSerializer):
    rows = PurchaseOrderRowSerializer(many=True)
    date = serializers.DateField(format=None)

    class Meta:
        model = PurchaseOrder


class HandoverRowSerializer(serializers.ModelSerializer):
    item_id = serializers.Field(source='item.id')

    class Meta:
        model = HandoverRow


class HandoverSerializer(serializers.ModelSerializer):
    rows = HandoverRowSerializer()
    date = serializers.DateField(format=None)

    class Meta:
        model = Handover


class EntryReportRowSerializer(serializers.ModelSerializer):
    item_id = serializers.Field(source='item.id')

    class Meta:
        model = EntryReportRow
        exclude = ['item']


class EntryReportSerializer(serializers.ModelSerializer):
    rows = EntryReportRowSerializer()

    class Meta:
        model = EntryReport


class InventoryAccountRowSerializer(serializers.ModelSerializer):
    id = serializers.Field(source='id')
    voucher_no = serializers.Field(source='creator.get_voucher_no')
    specification = serializers.Field(source='creator.specification')
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