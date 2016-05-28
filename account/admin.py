from models import JournalVoucher, JournalVoucherRow, Transaction, Account, JournalEntry, Receipt, ReceiptRow, Category, Party
from django.contrib import admin
from app.utils.translation import TranslationAdmin

class PartyAdmin(TranslationAdmin):
    list_display = ('__unicode__', 'address', 'phone_no', 'pan_no')
    list_display_links = ('__unicode__', 'pan_no', 'phone_no')
    search_fields = ('address', 'phone_no', 'pan_no')

admin.site.register(Party, PartyAdmin)

admin.site.register(JournalVoucher)
admin.site.register(JournalVoucherRow)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(JournalEntry)
admin.site.register(Receipt)
admin.site.register(ReceiptRow)
admin.site.register(Category)