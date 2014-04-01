from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=2000)
    stack_items = models.ManyToManyField("projects.StackItem")
    order_index = models.IntegerField(default=0)
    source_url = models.URLField(blank=True, default='')
    is_draft = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('order_index',)


class ProjectFeature(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, related_name='features')

    def __unicode__(self):
        return self.name


class StackItem(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250, blank=True, default='')

    def __unicode__(self):
        return self.name
