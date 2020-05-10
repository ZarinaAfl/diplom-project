from django import forms

from .models import Intervention, Param, ParamValue, Template


class PostForm(forms.ModelForm):
    class Meta:
        model = Intervention
        fields = ('name', 'annotation', 'sphere')

class ParamForm(forms.ModelForm):
    class Meta:
        model = Param
        fields = ('name', 'type')


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ('protocol',)


