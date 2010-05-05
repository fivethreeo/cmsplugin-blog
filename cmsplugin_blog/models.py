from django.db import models
from cms import settings
from cms.models.fields import PlaceholderField
import datetime

class PublishedEntriesManager(models.Manager):
    """
        Filters out all unpublished and items with a publication date in the future
    """
    def get_query_set(self):
        return super(PublishedEntriesManager, self).get_query_set() \
                    .filter(is_published=True, pub_date__lte=datetime.datetime.now())
                    
class Entry(models.Model):
    is_published = models.BooleanField()
    content = PlaceholderField('entry')
    pub_date = models.DateTimeField(default=datetime.datetime.now)
 
    objects = models.Manager()
    published = PublishedEntriesManager()

class EntryTitle(models.Model):
    entry = models.ForeignKey(Entry)
    language = models.CharField(max_length=2, choices=settings.LANGUAGES)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    
    def __unicode__(self):
        return self.title
        
    def __get_absolute_url(self):
        return ('blog_detail', (), {
            'year': self.entry.pub_date.strftime('%Y'),
            'month': self.entry.pub_date.strftime('%m'),
            'day': self.entry.pub_date.strftime('%d'),
            'slug': self.slug
        })
    _get_absolute_url = models.permalink(__get_absolute_url)
    
    def get_absolute_url(self):
        return u'/%s%s' % (self.language, self._get_absolute_url())
        
from cms.models import CMSPlugin

class PygmentsPlugin(CMSPlugin):
    code_language = models.CharField(max_length=20)
    code = models.TextField()
