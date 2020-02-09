from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import timezone

TYPE_PARAM = (
    (1, 'NUMBER'),
    (2, 'TEXT'),
    (3, 'FILE'),
    (4, 'IMAGE'),
)

SPHERE = (
    ('M', 'Математика'),
    ('R', 'Русский язык'),
    ('L', 'Литература'),
)


class Intervention(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True, verbose_name="Название интервенции")
    annotation = models.TextField(verbose_name="Описание интервенции")
    sphere = models.CharField(
        max_length=2,
        choices=SPHERE,
        default='MATHS', verbose_name="Тематическая область"
    )
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name


'''
class Request(models.Model):
    intervention = models.ForeignKey(Intervention,
                                    related_name='intervention_request', on_delete=models.CASCADE,
                                    blank=True, null=True, verbose_name='Конкурс')
    result_value = models.FloatField(default=0)

    class Meta:
        unique_together = (('competition', 'participant'),)

    def __str__(self):
        return "Заявка %s - %s" % (self.participant, self.competition.name)
'''


class Param(models.Model):
    intervention = models.ForeignKey(Intervention, related_name='intervention_parameters', on_delete=models.CASCADE,
                                     blank=False, null=False, verbose_name='Ссылка на интервенцию')
    name = models.CharField(max_length=70)
    type = models.IntegerField(choices=TYPE_PARAM, null=False, blank=False, default=TYPE_PARAM[0][0],
                               verbose_name='Тип параметра')

    def __str__(self):
        return "Параметр %s интервенции %s" % (self.name, self.intervention.name)


fs = FileSystemStorage(location='/media/images')

class ParamValue(models.Model):
    param = models.ForeignKey(Param, related_name='param_values', on_delete=models.CASCADE, blank=False, null=False,
                              verbose_name='Значение параметра')
    value = models.FloatField(default=0, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    #image = models.ImageField(storage=fs)
    file = models.FileField(null=True, blank=True)

    def is_number(self):
        return self.param.type == 1

    def is_file(self):
        return self.param.type == 3

    def is_image(self):
        return self.param.type == 4

    def get_name(self):
        return self.param.name

    def get_files(self):
        return self.files.all()
