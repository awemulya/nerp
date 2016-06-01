from models import JournalVoucher, JournalVoucherRow, Transaction, Account, JournalEntry, Receipt, ReceiptRow, Category
from django.contrib import admin

admin.site.register(JournalVoucher)
admin.site.register(JournalVoucherRow)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(JournalEntry)
admin.site.register(Receipt)
admin.site.register(ReceiptRow)
admin.site.register(Category)