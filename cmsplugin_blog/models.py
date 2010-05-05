from django.db import models
from cms import settings
from cms.models.fields import PlaceholderField

class Entry(models.Model):
    published = models.BooleanField()
    content = PlaceholderField('entry')

class EntryTitle(models.Model):
    entry = models.ForeignKey(Entry)
    language = models.CharField(max_length=2, choices=settings.LANGUAGES)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    
    def __unicode__(self):
        return self.title