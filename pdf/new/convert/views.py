from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic import View
import datetime

from convert.utils import render_to_pdf #created in step 4

class GeneratePdf(View):
     def get(self, request, *args, **kwargs):
         data = {
              'answer': "This is a demo . Answers will be lifted from database "
              
         }
         pdf = render_to_pdf('convert/answer.html', data)
         return HttpResponse(pdf, content_type='application/pdf')

#class GeneratePDF(View):
#     def get(self, request, *args, **kwargs):
#         template = get_template('invoice.html')
#         context = {
#             "invoice_id": 123,
#             "customer_name": "John Cooper",
#             "amount": 1399.99,
#             "today": "Today",
#         }
#         html = template.render(context)
#         pdf = render_to_pdf('invoice.html', context)
#         if pdf:
#             response = HttpResponse(convert, content_type='application/convert')
#             filename = "Invoice_%s.convert" %("12341231")
#             content = "inline; filename='%s'" %(filename)
#             download = request.GET.get("download")
#             if download:
#                 content = "attachment; filename='%s'" %(filename)
#             response['Content-Disposition'] = content
#             return response
#         return HttpResponse("Not found")
