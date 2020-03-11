from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required, permission_required
from .tasks import task_run
from Management.views import IndexView
from django.views.static import serve 
from django.conf import settings

urlpatterns = [
    url(r'^$', login_required(IndexView.as_view()), name = "index"),
    url(r'^admin/', admin.site.urls),
    url(r'^auths/', include('Auths.urls', app_name = 'auths', namespace='auths')),
    url(r'^manage/', include('Management.urls', app_name = 'manage', namespace='manage')),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]

task_run()