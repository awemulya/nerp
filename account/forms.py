from account.models import Account, Category
from app.utils.forms import HTML5BootstrapModelForm


class AccountForm(HTML5BootstrapModelForm):
    class Meta:
        model = Account
        exclude = ('parent', 'category')


class CategoryForm(HTML5BootstrapModelForm):
    class Meta:
        model = Category
        exclude = ('parent',)
