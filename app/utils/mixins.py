import os
from django.contrib import messages

from django.views.generic.edit import UpdateView as BaseUpdateView, CreateView as BaseCreateView, DeleteView as BaseDeleteView

from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from weasyprint import HTML, CSS


def json_from_object(obj):
    data = {
        'id': obj.id
    }

    if hasattr(obj, 'name'):
        data['name'] = obj.name
    elif hasattr(obj, 'title'):
        data['name'] = obj.title
    else:
        data['name'] = str(obj)

    if hasattr(obj, 'percent'):
        data['percent'] = obj.percent  # Percent attr for tax scheme
    return JsonResponse(data)


class AjaxableResponseMixin(object):
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            if 'ret' in self.request.GET:
                obj = getattr(self.object, self.request.GET['ret'])
            else:
                obj = self.object
            return json_from_object(obj)
        else:
            return response


def find_static(path):
    from django.contrib.staticfiles import finders
    from django.utils.encoding import smart_unicode

    result = finders.find(path, all=True)
    path = smart_unicode(path)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        output = u'\n  '.join(
            (smart_unicode(os.path.realpath(path)) for path in result))
        return output


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)


class PDFView(TemplateView):
    def get_file_name(self):
        filename = 'download'
        if hasattr(self, 'file_name') and self.file_name:
            filename = self.file_name
        if hasattr(self, 'template_name') and self.template_name:
            from os.path import basename, splitext

            filename = splitext(basename(self.template_name))[0]
        if not filename.endswith('.pdf'):
            filename += '.pdf'
        return filename

    def get_stylesheets(self):
        return [CSS(find_static('css/normalize.css')), CSS(find_static('css/bootstrap/bootstrap.min.css')),
                CSS(find_static('css/base.css')), CSS(find_static('css/pdf.css'))]

    def render_to_response(self, *args, **kwargs):
        html_template = get_template(self.template_name)
        context = {'you': self.request.user, 'pagesize': 'A4'}
        context.update(self.get_context_data())
        rendered_html = html_template.render(RequestContext(self.request, context)).encode(encoding="UTF-8")
        pdf_file = HTML(string=rendered_html).write_pdf(stylesheets=self.get_stylesheets())
        http_response = HttpResponse(pdf_file, content_type='application/pdf')
        http_response['Content-Disposition'] = 'filename="' + self.get_file_name()
        return http_response



class UpdateView(BaseUpdateView):
    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['scenario'] = _('Edit')
        context['base_template'] = 'base.html'
        super(UpdateView, self).get_context_data()
        return context


class CreateView(BaseCreateView):
    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['scenario'] = _('Add')
        if self.request.is_ajax():
            base_template = 'modal.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        return context


class DeleteView(BaseDeleteView):
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = super(DeleteView, self).post(request, *args, **kwargs)
        messages.success(request, ('%s %s' % (self.object.__class__._meta.verbose_name.title(), _('successfully deleted!'))))
        return response

class TableObjectMixin(TemplateView):
    def get_context_data(self, *args, **kwargs):
        context = super(TableObjectMixin, self).get_context_data(**kwargs)
        if self.kwargs:
            pk = int(self.kwargs.get('pk'))
            obj = get_object_or_404(self.model, pk=pk, company=self.request.company)
            scenario = 'Update'
        else:
            obj = self.model(company=self.request.company)
            # if obj.__class__.__name__ == 'PurchaseVoucher':
            #     tax = self.request.company.settings.purchase_default_tax_application_type
            #     tax_scheme = self.request.company.settings.purchase_default_tax_scheme
            #     if tax:
            #         obj.tax = tax
            #     if tax_scheme:
            #         obj.tax_scheme = tax_scheme
            scenario = 'Create'
        data = self.serializer_class(obj).data
        context['data'] = data
        context['scenario'] = scenario
        context['obj'] = obj
        return context

