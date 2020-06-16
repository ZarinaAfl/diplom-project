from django import forms

from .models import Intervention, IntervParam, ParamValue, Template


class PostForm(forms.ModelForm):
    class Meta:
        model = Intervention
        fields = ('name', 'annotation', 'subject')

class ParamForm(forms.ModelForm):
    class Meta:
        model = IntervParam
        fields = ('name', 'type')


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ('protocol',)


