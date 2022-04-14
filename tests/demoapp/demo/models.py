from django.db import models


class DemoModel1(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Button Example'
        verbose_name_plural = 'Button Examples'

    def __unicode__(self):
        return "DemoModel1 #%s" % self.pk

    def __str__(self):
        return "DemoModel1 #%s" % self.pk


class DemoModel2(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Link Example'
        verbose_name_plural = 'Link Examples'

    def __unicode__(self):
        return "DemoModel2 #%s" % self.pk

    def __str__(self):
        return "DemoModel2 #%s" % self.pk


class DemoModel3(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'View Example'
        verbose_name_plural = 'View Examples'


class DemoModel4(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Wizard Example'
        verbose_name_plural = 'Wizard Examples'


class DemoModel5(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Choice Example'
        verbose_name_plural = 'Choice Examples'

