from django.contrib import admin
from .models import Intervention, Param, ParamValue, Template, TemplParam, Research, ResearchParamValue

admin.site.register(Intervention)
admin.site.register(Param)
admin.site.register(ParamValue)
admin.site.register(Template)
admin.site.register(TemplParam)
admin.site.register(Research)
admin.site.register(ResearchParamValue)

