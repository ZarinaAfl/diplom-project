from django.contrib import admin
from .models import Intervention, Param, ParamValue #UploadData

admin.site.register(Intervention)
admin.site.register(Param)
admin.site.register(ParamValue)
#admin.site.register(UploadData)