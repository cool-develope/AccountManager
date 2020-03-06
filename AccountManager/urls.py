from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auths/', include('Auths.urls', app_name = 'auths', namespace='auths')),
    url(r'^manage/', include('Management.urls', app_name = 'manage', namespace='manage')),
]