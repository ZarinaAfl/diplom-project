from django import forms

from .models import Intervention, Param, ParamValue


class PostForm(forms.ModelForm):
    class Meta:
        model = Intervention
        fields = ('name', 'annotation', 'sphere')

class ParamForm(forms.ModelForm):
    class Meta:
        model = Param
        fields = ('name', 'type')


class ParamFileForm(forms.ModelForm):
    class Meta:
        model = ParamValue
        fields = [
            "param",
            "value",
            "text",
            "file"
        ]