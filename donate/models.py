from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200)
    reg_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.name