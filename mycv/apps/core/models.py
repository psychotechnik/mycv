from django.db import models


class Address(models.Model):

    street_address = models.CharField(max_length=250, blank=True)
    street_address2 = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(blank=True, max_length=10)

    def __unicode__(self):
        return "%s" % self.formatted_address

    @property
    def formatted_address(self):
        return "%s %s %s %s" % (self.street_address, self.city or '', self.state or '', self.zip_code or '')