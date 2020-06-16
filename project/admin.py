from django.contrib import admin
from .models import Intervention, IntervParam, ParamValue, Template, TemplParam, Research, ResearchParamValue, StageResearch, \
    TaskStage, CustomUser, EducatInst, ResponsTask


admin.site.register(Intervention)
admin.site.register(IntervParam)
admin.site.register(ParamValue)
admin.site.register(Template)
admin.site.register(TemplParam)
admin.site.register(Research)
admin.site.register(ResearchParamValue)
admin.site.register(StageResearch)
admin.site.register(TaskStage)
admin.site.register(CustomUser)
admin.site.register(EducatInst)
admin.site.register(ResponsTask)