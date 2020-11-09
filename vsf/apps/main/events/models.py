# WARNING: There's a lot of fields that require to be checked at some point,
# they're marked with a @TODO, please fix this configuration before launching 
# the production build

# coding=utf-8
from __future__ import unicode_literals

from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=50, null=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return u'%s' % self.name

class State(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(    to=Country, 
                                    on_delete=models.CASCADE, #@TODO FOR DEBUG ONLY
                                    related_name='states')

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"
        unique_together = (("name", "country"),)

    def __str__(self):
        return u'%s' % self.name

class MutedInput(models.Model):

    MED = 'MED'
    DNS = 'DNS'
    TCP = 'TCP'
    HTTP = 'HTTP'

    TYPE_CHOICES = (
        (MED, 'Medicion'),
        (DNS, 'Medicion DNS'),
        (TCP, 'Medicion TCP'),
        (HTTP, 'Medicion HTTP')
    )

    url = models.CharField(max_length=50, null=True) #@TODO why not urlfield ?
    type_med = models.CharField(verbose_name='Tipo de Medicion',
                                max_length=50,
                                choices=TYPE_CHOICES,
                                default=MED)

    def __str__(self):
        return u"%s - %s" % (self.url, self.type_med)

class ISP(models.Model):
    name = models.CharField(max_length=100, unique=True) # ASN is not required?

    def __str__(self):
        return u"%s" % self.name

class Plan(models.Model):
    name = models.CharField(max_length=100)
    isp =   models.ForeignKey(
                                to=ISP,
                                on_delete=models.CASCADE #@TODO debug only, do not build  for production
                            )
    upload = models.CharField(
        verbose_name='Velocidad de Carga publicitado',
        max_length=30)
    download = models.CharField(
        verbose_name='Velocidad de Descarga publicitado',
        max_length=30)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return u"%s" % self.name

class SiteCategory(models.Model):

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    abbreviation = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return u"%s" % self.name

class Site(models.Model):

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
                                    to=SiteCategory,
                                    on_delete=models.SET_NULL, #@TODO for debug only
                                    null=True,
                                    blank=True
                                )

    def __str__(self):
        return u"%s" % self.name

class Target(models.Model):

    DOMAIN = 'domain'
    URL = 'url'
    IP = 'ip'

    TYPE = (
        (DOMAIN, 'Domain'),
        (URL, 'Url'),
        (IP, 'Ip')
    )

    site = models.ForeignKey(
        to=Site, null=True, blank=True, related_name='targets',
        on_delete=models.CASCADE #@TODO For debug only
    )
    domain = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    type = models.CharField(choices=TYPE, default=DOMAIN, max_length=10)

    def __str__(self):

        if self.type == self.DOMAIN:
            return u"%s -> %s" % (self.type, self.domain)
        elif self.type == self.URL:
            return u"%s -> %s" % (self.type, self.url)
        elif self.type == self.IP:
            return u"%s -> %s" % (self.type, self.ip)

class Event(models.Model):

    NONE = 'none'
    TCP = 'tcp'
    DNS = 'dns'
    HTTP = 'http'
    NDT = 'ndt'

    TYPE = {
        NONE: 'none',
        TCP: 'tcp',
        DNS: 'dns',
        HTTP: 'http',
        NDT: 'ndt'
    }
    TYPE_CHOICES = [    # Items are sorted alphabetically
        (k, v) for k, v in sorted(TYPE.items(), key=lambda t: t[1])]

    TYPES = (
        ('bloqueo por DPI', 'bloqueo por DPI'),
        ('bloqueo por DNS', 'bloqueo por DNS'),
        ('bloqueo por IP', 'bloqueo por IP'),
        ('Interceptacion de trafico', 'Interceptación de tráfico'),
        ('falla de dns', 'falla de dns'),
        ('Velocidad de internet', 'Velocidad de internet'),
        ('alteracion de trafico por intermediarios', 'alteración de tráfico por intermediarios')
    )

    isp = models.ForeignKey(
                            to=ISP,
                            on_delete=models.SET_NULL, #@TODO for debug only
                            null=True,
                            blank=True
                        )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    target = models.ForeignKey( to=Target, # input in metrics
                                on_delete=models.CASCADE #@TODO ONLY DEBUGGING
                                )
    region = models.ForeignKey( to=State, 
                                on_delete=models.SET_NULL, #@TODO ONLY DEBUG
                                null=True,
                                blank=True
                            )
    identification = models.CharField(max_length=50, unique=True)
    draft = models.BooleanField(default=True)
    public_evidence = models.TextField(null=True, blank=True)
    private_evidence = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=100, choices=TYPES)
    plugin_name = models.CharField(max_length=100, null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        return super(Event, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                       update_fields=update_fields)

    def __str__(self):
        return u"%s" % self.identification
