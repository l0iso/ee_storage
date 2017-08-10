import os
from django.http import QueryDict, HttpResponseForbidden
from django.shortcuts import HttpResponse
from django.core.files.storage import default_storage
from django.utils._os import safe_join
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


def file_exist(path):
    full_path = safe_join(settings.MEDIA_ROOT, path)
    result = os.path.exists(full_path)
    return result


@csrf_exempt
def upload(request):
    if request.method == 'POST':
        files = request.FILES
        print(request.POST.get('file_name'))
        if not file_exist(request.POST.get('file_name')):
            default_storage.save(name=request.POST.get('file_name'), content=files.get('file'))
            return HttpResponse()
        else:
            return HttpResponseForbidden('error')
    if request.method == 'GET':
        data = request.GET
        if data.get('path'):
            result = file_exist(data['path'])
            return HttpResponse(result)
    return HttpResponse()

