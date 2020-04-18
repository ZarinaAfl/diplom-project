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

SPHERE = (
    ('M', 'Математика'),
    ('R', 'Русский язык'),
    ('L', 'Литература'),
)

class CustomUser(models.Model):
    fullname = models.CharField(max_length=100, verbose_name="ФИО", default="")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='custom_user')
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
    sphere = models.CharField(
        max_length=2,
        choices=SPHERE,
        default='MATHS', verbose_name="Дисциплина"
    )
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name


class Param(models.Model):
    intervention = models.ForeignKey(Intervention, related_name='intervention_parameters', on_delete=models.CASCADE,
                                     blank=False, null=False, verbose_name='Ссылка на интервенцию')
    name = models.CharField(max_length=70)
    type = models.IntegerField(choices=TYPE_PARAM, null=False, blank=False, default=TYPE_PARAM[0][0],
                               verbose_name='Тип параметра')

    def __str__(self):
        return "Параметр %s интервенции %s" % (self.name, self.intervention.name)


class ParamValue(models.Model):
    param = models.ForeignKey(Param, related_name='param_values', on_delete=models.CASCADE, blank=False, null=False,
                              verbose_name='Значение параметра')
    value = models.IntegerField(default=0, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    file = models.FileField(default='file')
    image = models.ImageField(default='image')

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

    def get_files(self):
        return self.files.all()


class Template(models.Model):
    intervention = models.ForeignKey(Intervention, related_name='research_template', on_delete=models.CASCADE,
                                     blank=False, null=False, verbose_name='Шаблон исследования')
    description = models.TextField(verbose_name="Описание")
    formula = models.TextField(blank=True, null=True)


class TemplParam(models.Model):
    template = models.ForeignKey(Template, related_name='template_param', on_delete=models.CASCADE,
                                 blank=False, null=False, verbose_name='Параметр исследования')
    name = models.CharField(max_length=70, default='test')
    type = models.IntegerField(choices=TYPE_PARAM, null=False, blank=False, default=TYPE_PARAM[0][0],
                               verbose_name='Тип параметра')


class Research(models.Model):
    intervention = models.ForeignKey(Intervention, related_name='research_interv', on_delete=models.CASCADE,
                                 blank=False, null=False, verbose_name='Исследование интервенции', default=None)
    template = models.ForeignKey(Template, related_name='template', on_delete=models.CASCADE,
                                 blank=False, null=False)
    name = models.CharField(max_length=70, default='test')
    effect = models.IntegerField(verbose_name='Эффективность интервенции по исследованию', default=0)


class ResearchParamValue(models.Model):
    research = models.ForeignKey(Research, related_name='research', on_delete=models.CASCADE, blank=False, null=False)

    param = models.ForeignKey(TemplParam, related_name='templ_param', on_delete=models.CASCADE, blank=False, null=False)

    value = models.FloatField(default=0, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    file = models.FileField(default='file')
    image = models.ImageField(default='image')

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

    # def get_files(self):
    #   return self.files.all()
