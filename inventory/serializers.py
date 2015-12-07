from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from core.serializers import PartySerializer
from inventory.models import PartyQuotation, QuotationComparison, QuotationComparisonRow, Demand, DemandRow, Item, PurchaseOrder, \
    PurchaseOrderRow, HandoverRow, Handover, \
    EntryReport, EntryReportRow, JournalEntry, InspectionRow, Inspection, Transaction, ItemLocation, Depreciation, \
    ItemInstance, \
    Release, YearlyReport, YearlyReportRow


class YearlyReportRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearlyReportRow


class YearlyReportSerializer(serializers.ModelSerializer):
    rows = YearlyReportRowSerializer(many=True)

    class Meta:
        model = YearlyReport


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
    id = serializers.ReadOnlyField()
    voucher_no = serializers.SerializerMethodField()
    specification = serializers.SerializerMethodField()
    country_or_company = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    expected_life = serializers.SerializerMethodField()
    source = serializers.SerializerMethodField()
    income_quantity = serializers.SerializerMethodField()
    income_rate = serializers.SerializerMethodField()
    income_total = serializers.SerializerMethodField()
    expense_quantity = serializers.SerializerMethodField()
    # expense_total_cost_price = serializers.SerializerMethodField()
    remaining_total_cost_price = serializers.SerializerMethodField()
    remarks = serializers.SerializerMethodField()
    current_balance = serializers.SerializerMethodField()
    date = serializers.DateField(format=None)
    creator_type = serializers.SerializerMethodField()

    # expense_total = serializers.ReadOnlyField(source='account_row.expense_total')

    expense_total = serializers.SerializerMethodField()

    def get_voucher_no(self, obj):
        if hasattr(obj.creator, 'voucher_no'):
            return obj.creator.voucher_no
        elif hasattr(obj.creator, 'get_voucher_no'):
            return obj.creator.get_voucher_no()
        else:
            return ''

    def get_specification(self, obj):
        if hasattr(obj.creator, 'specification'):
            return obj.creator.specification
        else:
            return ''

    def get_creator_type(self, obj):
        return obj.creator.__class__.__name__.replace('Row', '')

    def get_expense_total(self, obj):
        if obj.creator.__class__.__name__ == 'Expense':
            return obj.creator.rate
        try:
            if obj.account_row.expense_total_cost_price:
                return obj.account_row.expense_total_cost_price
        except ObjectDoesNotExist:
            pass
        total = 0
        if obj.creator.__class__.__name__ == 'DemandRow':
            for release in obj.creator.releases.all():
                total += release.item_instance.rate
            return total
        return 0

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
        if obj.creator.__class__.__name__ in ['DemandRow', 'Expense']:
            return ''
        return obj.creator.quantity

    def get_income_rate(self, obj):
        if obj.creator.__class__.__name__ in ['DemandRow', 'Expense']:
            return ''
        return obj.creator.rate

    def get_income_total(self, obj):
        if obj.creator.__class__ == DemandRow:
            return ''
        if obj.creator.__class__.__name__ == 'Expense':
            return ''

        # if obj.creator.__class__.__name__ == 'HandoverRow':
        #     if obj.creator.handover
        #     return obj.creator.total_amount
        return obj.creator.total_entry_cost()

    def get_expense_quantity(self, obj):
        if obj.creator.__class__.__name__ in ['EntryReportRow']:
            return ''
        if obj.creator.__class__.__name__ in ['Expense']:
            return 1

        return obj.creator.release_quantity

    # def get_expense_total_cost_price(self, obj):
    #     try:
    #         return obj.account_row.expense_total_cost_price or ''
    #     except:
    #         return ''

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
        if obj.creator.__class__.__name__ in ['Expense']:
            account = obj.creator.instance.item.account
        else:
            account = obj.creator.item.account
        return obj.transactions.filter(account=account)[0].current_balance


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


class PartyQuotationSerializer(serializers.ModelSerializer):
    party = PartySerializer()

    class Meta:
        model = PartyQuotation


class QuotationComparisonRowSerializer(serializers.ModelSerializer):
    bidder_quote = PartyQuotationSerializer(many=True)
    item_id = serializers.ReadOnlyField(source='item.id')

    class Meta:
        model = QuotationComparisonRow
        exclude = ['item']


class QuotationComparisonSerializer(serializers.ModelSerializer):
    rows = QuotationComparisonRowSerializer(many=True)

    class Meta:
        model = QuotationComparison
