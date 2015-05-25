from datetime import date
import json
from core import app_setting
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from account.models import Receipt, ReceiptRow
from account.serializers import ReceiptSerializer
from app.utils.helpers import save_model, invalid
from inventory.models import delete_rows


def receipt(request, pk=None):
    if pk:
        obj = get_object_or_404(Receipt, pk=pk)
        scenario = 'Update'
    else:
        obj = Receipt(date=date.today())
        scenario = 'New'
    data = ReceiptSerializer(obj).data
    return render(request, 'receipt.html', {'scenario': scenario, 'data': data})


def save_receipt(request):
    params = json.loads(request.body)
    dct = {'rows': {}}
    object_values = {'no': params.get('no'), 'fiscal_year': app_setting.fiscal_year,
                     'date': params.get('date')}
    if params.get('id'):
        obj = Receipt.objects.get(id=params.get('id'))
    else:
        obj = Receipt()
    try:
        obj = save_model(obj, object_values)
    except Exception as e:
        if hasattr(e, 'messages'):
            dct['error_message'] = '; '.join(e.messages)
        elif str(e) != '':
            dct['error_message'] = str(e)
        else:
            dct['error_message'] = 'Error in form data!'
    dct['id'] = obj.id
    model = ReceiptRow
    for index, row in enumerate(params.get('table_view').get('rows')):
        if invalid(row, ['budget_head_id', 'account_id', 'tax_scheme_id']):
            continue
        values = {'sn': index + 1, 'budget_head_id': row.get('budget_head_id'),
                  'account_id': row.get('account_id'), 'invoice_no': row.get('invoice_no'),
                  'nepal_government': row.get('nepal_government'), 'foreign_cash_grant': row.get('foreign_cash_grant'),
                  'foreign_compensating_grant': row.get('foreign_compensating_grant'),
                  'foreign_cash_loan': row.get('foreign_cash_loan'),
                  'foreign_compensating_loan': row.get('foreign_compensating_loan'),
                  'foreign_substantial_aid': row.get('foreign_substantial_aid'),
                  'advanced': row.get('advanced'), 'cash_returned': row.get('cash_returned'),
                  'advanced_settlement': row.get('advanced_settlement'), 'vattable': row.get('vattable'),
                  'tax_scheme_id': row.get('tax_scheme_id'), 'activity_id': row.get('activity_id'),
                  'remarks': row.get('remarks'), 'receipt': obj}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['rows'][index] = submodel.id
    delete_rows(params.get('table_view').get('deleted_rows'), model)
    return JsonResponse(dct)