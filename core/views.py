import os
from django.http import QueryDict, HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import HttpResponse
from django.core.files.storage import default_storage
from django.utils._os import safe_join
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils.encoding import smart_str


def file_exist(path):
    full_path = safe_join(settings.MEDIA_ROOT, path)
    result = os.path.exists(full_path)
    return result


@csrf_exempt
def upload(request):
    if request.method == 'POST':
        files = request.FILES
        name = request.POST.get('file_name')
        print(name)
        if not file_exist(name):
            if request.POST.get('action') == 'create':
                result = default_storage.save(name=request.POST.get('file_name'), content=files.get('file'))
                return HttpResponse(result)
            else:
                return HttpResponseForbidden('error')
        else:
            return HttpResponseForbidden('file exists')


    if request.method == 'GET':
        data = request.GET
        if request.GET.get('action') == 'exists':
            if data.get('name'):
                result = default_storage.exists(data['name'])
                return HttpResponse(result)
        elif request.GET.get('action') == 'delete':
            if default_storage.exists(data['name']):
                default_storage.delete(name=data['name'])
            else:
                return HttpResponseNotFound('file not found')
        elif request.GET.get('action') == 'path':
            if default_storage.exists(data['name']):
                result = default_storage.path(name=data['name'])
                return HttpResponse(result)
            else:
                HttpResponseNotFound('file not found')
        else:
            return HttpResponseForbidden('no actions')

    return HttpResponse()


@csrf_exempt
def download(request):
    if request.method == 'GET':
        data = request.GET
        name = data.get('name')
        if default_storage.exists(name):
            response = HttpResponse(default_storage.open(data['name']),
                                    content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=%s' % data['name'].split('/')[-1]
            # response['X-Sendfile'] = default_storage.path(name=data['name'])
            # print(response.content)
            # for m in dir(response):
            #     print('method:', m)
            #     print('-----', getattr(response, m))
            return response
        else:
            return HttpResponseForbidden('file no exists')
    else:
        return HttpResponseForbidden('request error')
