"""apps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from .views import root


################################################################
# debug post request parameters

#from django.views.decorators.csrf import csrf_exempt

#@csrf_exempt
#def debug(request):
#    from django.http import HttpResponse
#    return HttpResponse(request.body, content_type="text/plain")

################################################################


urlpatterns = [
#    path('debug/', debug),

    path('', root, name='root'),
    path('users/', include('users.urls', namespace='users')),

    # path('admin/', admin.site.urls),
]
