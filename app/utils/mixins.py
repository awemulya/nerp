import os
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.staticfiles.templatetags.staticfiles import static

from weasyprint import HTML, CSS


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