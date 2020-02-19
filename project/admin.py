from django.contrib import admin
from .models import Intervention, Param, ParamValue, Template, TemplParam

admin.site.register(Intervention)
admin.site.register(Param)
admin.site.register(ParamValue)
admin.site.register(Template)
admin.site.register(TemplParam)
