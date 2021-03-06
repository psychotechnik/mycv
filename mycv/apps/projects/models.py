from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class Client(models.Model):
    CLIENT_TITLE_CHOICES = (
        (1, _("Consultant")),
        (2, _("Lead Developer")),
        #(3, _("")),
        #(4, _("")),
    )
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('applicant'),
        related_name="clients",
        null=True, blank=True,
    )
    title = models.IntegerField(max_length=2, choices=CLIENT_TITLE_CHOICES)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=2000)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    website = models.URLField(blank=True, default='')
    order_index = models.IntegerField(default=0)
    is_draft = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('order_index', '-end_date',)


class ClientObjective(models.Model):
    title = models.CharField(max_length=500)
    client = models.ForeignKey(Client, related_name='objectives')
    order_index = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=2000)
    stack_items = models.ManyToManyField("projects.StackItem")
    order_index = models.IntegerField(default=0)
    source_url = models.URLField(blank=True, default='')
    is_draft = models.BooleanField(default=True)
    client = models.ForeignKey(Client, related_name='projects', null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('order_index',)


class ProjectFeature(models.Model):
    name = models.CharField(max_length=500)
    project = models.ForeignKey(Project, related_name='features')

    def __unicode__(self):
        return self.name


class StackItem(models.Model):
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('applicant'),
        related_name="stack_items",
        null=True, blank=True,
    )
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250, blank=True, default='')

    def __unicode__(self):
        return self.name


class Skill(models.Model):
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('applicant'),
        related_name="skills",
        null=True, blank=True,
    )
    category = models.ForeignKey('categories.Category', null=True, blank=True)
    description = models.TextField(max_length=500, blank=True, default='')

    def __unicode__(self):
        return self.description
