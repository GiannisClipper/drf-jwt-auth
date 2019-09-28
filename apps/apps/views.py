from django.http import HttpResponse

def root(req):
    return HttpResponse('DRF-JWT-AUTH welcomes you!', content_type="text/plain")