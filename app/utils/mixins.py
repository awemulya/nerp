from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse
from django.views.generic import TemplateView

from weasyprint import HTML


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

    def render_to_response(self, *args, **kwargs):
        html_template = get_template(self.template_name)
        context = {'you': self.request.user, 'pagesize': 'A4'}
        context.update(self.get_context_data())
        rendered_html = html_template.render(RequestContext(self.request, context)).encode(encoding="UTF-8")
        pdf_file = HTML(string=rendered_html).write_pdf()
        http_response = HttpResponse(pdf_file, content_type='application/pdf')
        http_response['Content-Disposition'] = 'filename="' + self.get_file_name()
        return http_response
