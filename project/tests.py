class Stage(models.Model):
    stage = models.ForeignKey(StageResearch, on_delete=models.CASCADE, default=None)
    responsible = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)

organization = models.ForeignKey(EducatInst, on_delete=models.CASCADE, default=None)
