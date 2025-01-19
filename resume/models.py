from django.db import models

# Create your models here.
class Data(models.Model):
    job_desc = models.TextField()
    resume_file = models.FileField()
