from django.db import models

# Create your models here.
from django.db       import models

class House(models.Model):
    CRIM    = models.FloatField()
    ZN      = models.FloatField()
    INDUS   = models.FloatField()
    CHAS    = models.FloatField()
    NOX     = models.FloatField()
    RM      = models.FloatField()
    AGE     = models.FloatField()
    DIS     = models.FloatField()
    RAD     = models.FloatField()
    TAX     = models.FloatField()
    PTRATIO = models.FloatField()
    B       = models.FloatField()
    LSTAT   = models.FloatField()
    MEDV    = models.FloatField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
      	ordering = ['created']
