#__author:  Administrator
#date:   2019/3/1

from django.utils.deprecation import MiddlewareMixin
from .visit_info import visit_info

class VisitMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        print(response.status_code in (200,301,302))
        if response.status_code in (200,301,302) and '/admin/' not in request.path:
            visit_info(request, '/')
            print (12121)
        return response
