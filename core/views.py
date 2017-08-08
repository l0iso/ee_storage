from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from ee_storage import urls
from . import models, forms
# Create your views here.


def upload(request):
    obj_list = models.CustomFile.objects.all()
    if request.method == 'POST':
        form = forms.CustomForm(request.POST, request.FILES)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect(reverse('upload'))
    else:
        form = forms.CustomForm()
    return render(request, 'core/custom.html', locals())


def del_objects(request):
    objs = models.StandardFile.objects.all()
    objs.delete()
    return redirect(reverse('upload'))


def std_upload(request):
    obj_list = models.StandardFile.objects.all()
    print(obj_list, 'kekfe')
    if request.method == 'POST':
        form = forms.StandardForm(request.POST, request.FILES)
        print(form, form.is_valid(), request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect(reverse('std_upload'))
    else:
        form = forms.StandardForm()
    return render(request, 'core/custom.html', locals())
