from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

EXEMPT_URLS = ['/']
class LoginRequiredMiddleware(MiddlewareMixin):
    
    def process_request(self, request):  
        if not request.user.is_authenticated:
            if request.path not in EXEMPT_URLS:
                return HttpResponseRedirect("/")