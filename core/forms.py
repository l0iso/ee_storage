from django import forms
from . import models


class CustomForm(forms.ModelForm):

    class Meta:
        model = models.CustomFile
        fields = '__all__'


class StandardForm(forms.ModelForm):

    class Meta:
        model = models.StandardFile
        fields = '__all__'


class SecondForm(forms.ModelForm):

    class Meta:
        model = models.Second
        fields = '__all__'
        