#-*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
#encoding= utf-8

# Create your models here.

class Image( models.Model ):
    image = models.ImageField( upload_to="" )
    name = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.name="/media/"+self.image.name
            #This code only happens if the objects is
            #not in the database yet. Otherwise it would
            #have pk
        super(Image, self).save(*args, **kwargs)

    def __unicode__( self ):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name

class EntryQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published=True)



class Entry(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)
    published = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)
    objects = EntryQuerySet.as_manager()
    images = models.ManyToManyField(Image)

    def get_absolute_url(self):
        return reverse("entry_detail", kwargs={"slug":self.slug})

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "Post del Blog"
        verbose_name_plural= "Posts del Blog"
        ordering = ["-created_date"]

class Carousel(models.Model):
    image = models.ImageField( upload_to="/carousel" )
    text = models.CharField(max_length=100)
    entry = models.ForeignKey(Entry)

class Comment(models.Model):
    text = models.CharField(max_length=100)
    post = models.ForeignKey(Entry)
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Comentario de "+self.name