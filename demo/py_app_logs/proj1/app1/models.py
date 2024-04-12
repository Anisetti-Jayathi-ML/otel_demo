from django.db import models
from django_extensions.db.fields import RandomCharField
from jsonfield import JSONField

# Create your models here.


class ProjectModel(models.Model):
    """
    Project model definition
    """
    id = RandomCharField(length=10, primary_key=True)
    project_name = models.CharField(max_length=64, null=True)
    description = models.TextField(null=True)
    owner = models.TextField(null=True)
    objects = models.Manager()

    class Meta:
        db_table = 'project'
        app_label = 'app1'
    

class AppModel(models.Model):
    id = RandomCharField(length=10, primary_key=True)
    application_name = models.CharField(max_length=64, null=True)
    application_type = models.TextField(null=True)
    description = models.TextField(null=True)
    project_id = models.TextField(null=True)

    class Meta:
        db_table = 'application'
        app_label = 'app1'
