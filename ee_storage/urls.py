from django.conf.urls import include, url
from django.views.static import serve
from rest_framework import routers
from django.contrib import admin
from core import views
from django.conf import settings

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^download/$', views.download, name='download'),

]

if settings.DEBUG:
    # media files (images) for dev server
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]