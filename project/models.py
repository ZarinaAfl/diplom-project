import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import timezone

fs = FileSystemStorage(location='/media/images')

TYPE_PARAM = (
    (1, 'NUMBER'),
    (2, 'TEXT'),
    (3, 'FILE'),
    (4, 'IMAGE'),
)
ROLE_CHOICES = (
    (1, 'Администратор'),
    (2, 'Автор интервенции'),
    (3, 'Исследователь'),
)

SUBJECT = (
    ('M', 'Математика'),
    ('I', 'Информатика'),
    ('R', 'Русский язык'),
    ('L', 'Литература'),
    ('F', 'Иностранный язык'),
)

STATUS = (
    ('in work', 'В работе'),
    ('completed', 'Завершено'),
    ('canceled', 'Отменено'),
)


class EducatInst(models.Model):
    name = models.CharField(max_length=255, verbose_name="Образовательное учреждение")

    def __str__(self):
        return self.name


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='custom_user')
    fullname = models.CharField(max_length=100, verbose_name="ФИО")
    organization = models.ForeignKey(EducatInst, on_delete=models.CASCADE, verbose_name="Образовательное учреждение")
    role = models.IntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=ROLE_CHOICES[0][0],
                               verbose_name="Роль")

    def __str__(self):
        return self.fullname

    def get_username(self):
        return self.fullname


class Intervention(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True, verbose_name="Название")
    annotation = models.TextField(verbose_name="Описание")
    subject = models.CharField(
        max_length=2,
        choices=SUBJECT,
        default='MATHS', verbose_name="Дисциплина"
    )
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class IntervParam(models.Model):
    intervention = models.ForeignKey(Intervention, related_name='intervention_parameters', on_delete=models.CASCADE,
                                     blank=False, null=False, verbose_name='Интервенция параметра')
    name = models.CharField(max_length=70)
    type = models.IntegerField(choices=TYPE_PARAM, null=False, blank=False, default=TYPE_PARAM[0][0],
                               verbose_name='Тип параметра')

    def __str__(self):
        return "Параметр %s интервенции %s" % (self.name, self.intervention.name)


class ParamValue(models.Model):
    param = models.ForeignKey(IntervParam, related_name='param_values', on_delete=models.CASCADE, blank=False,
                              null=False,
                              verbose_name='Значение параметра', default='')
    value = models.IntegerField(default=0, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    file = models.FileField()
    image = models.ImageField()

    def filename(self):
        return os.path.basename(self.file.name)

    def is_number(self):
        return self.param.type == 1

    def is_text(self):
        return self.param.type == 2

    def is_file(self):
        return self.param.type == 3

    def is_image(self):
        return self.param.type == 4

    def get_name(self):
        return self.param.name


class Template(models.Model):
    intervention = models.ForeignKey(Intervention, related_name='research_template', on_delete=models.CASCADE,
                                     blank=False, null=False, verbose_name='Шаблон исследования')
    formula = models.TextField(blank=True, null=True)
    protocol = models.FileField(default='file')

    def __str__(self):
        return "Шаблон исследования интервенции " + self.intervention.name


class TemplParam(models.Model):
    template = models.ForeignKey(Template, related_name='template_param', on_delete=models.CASCADE,
                                 blank=False, null=False, verbose_name='Параметр исследования')
    name = models.CharField(max_length=70, default='test')
    type = models.IntegerField(choices=TYPE_PARAM, null=False, blank=False, default=TYPE_PARAM[0][0],
                               verbose_name='Тип параметра')

    def __str__(self):
        return self.name


class Research(models.Model):
    name = models.CharField(max_length=255)
    intervention = models.ForeignKey(Intervention, related_name='research_interv', on_delete=models.CASCADE,
                                     blank=False, null=False, verbose_name='Исследование интервенции')
    template = models.ForeignKey(Template, related_name='template', on_delete=models.CASCADE,
                                 blank=False, null=False)
    effect = models.FloatField(verbose_name='Эффективность интервенции по исследованию', default=0)
    organization = models.ForeignKey(EducatInst, related_name='org_research', default=None, on_delete=models.SET_NULL,
                                     null=True)
    status = models.CharField(choices=STATUS, max_length=50, blank=True, null=True, default=STATUS[0][0],
                              verbose_name="Статус")
    responsible = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class ResearchParamValue(models.Model):
    research = models.ForeignKey(Research, related_name='research', on_delete=models.CASCADE, blank=False, null=False)
    param = models.ForeignKey(TemplParam, related_name='templ_param', on_delete=models.CASCADE, blank=False, null=False)
    value = models.FloatField(default=0, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    file = models.FileField()
    image = models.ImageField()

    def filename(self):
        return os.path.basename(self.file.name)

    def is_number(self):
        return self.param.type == 1

    def is_text(self):
        return self.param.type == 2

    def is_file(self):
        return self.param.type == 3

    def is_image(self):
        return self.param.type == 4

    def __str__(self):
        return self.param.name


class StageResearch(models.Model):
    template = models.ForeignKey(Template, related_name='stage_research', on_delete=models.CASCADE,
                                 blank=False, null=False, verbose_name='Этап исследования')
    number = models.IntegerField(verbose_name="Номер этапа")
    name = models.CharField(max_length=255)

    def __str__(self):
        return "Стадия \"%s\" исследования интервенции \"%s\"" % (self.name, self.template.intervention.name)


#class Stage(models.Model):
 #   stage = models.ForeignKey(StageResearch, on_delete=models.CASCADE, null=False)


class TaskStage(models.Model):
    stage = models.ForeignKey(StageResearch, related_name='task_stage', on_delete=models.CASCADE,
                              blank=False, null=False, verbose_name='Этап задачи')
    number = models.IntegerField(verbose_name="Номер задачи")
    name = models.CharField(max_length=255)

    def __str__(self):
        return "Задача \"%s\" стадии \"%s\"" % (self.name, self.stage.name)


class ResponsTask(models.Model):
    research = models.ForeignKey(Research, related_name='task_stage', on_delete=models.CASCADE,
                                 blank=False, null=False, verbose_name='Исследование')
    taskstage = models.ForeignKey(TaskStage, related_name='task_stage', on_delete=models.CASCADE,
                                  blank=False, null=False, verbose_name='Этап задачи')
    responsible = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    status = models.CharField(choices=STATUS, max_length=50, blank=True, null=True, default=STATUS[0][0],
                              verbose_name="Статус")
    report = models.FileField(null=True)

    def is_completed(self):
        if self.report:
            return True
        else:
            return False
