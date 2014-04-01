from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=2000)
    is_draft = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name
