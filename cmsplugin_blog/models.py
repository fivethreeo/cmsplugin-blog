from django.utils.translation import ugettext_lazy as _

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
    
    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')
        ordering = ('-pub_date', )

class EntryTitle(models.Model):
    entry = models.ForeignKey(Entry)
    language = models.CharField(max_length=2, choices=settings.LANGUAGES)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    
    def __unicode__(self):
        return self.title
        
    def _get_absolute_url(self):
        language_namespace = 'simple_translation.middleware.MultilingualGenericsMiddleware' in settings.MIDDLEWARE_CLASSES and '%s:' % self.language
        return ('%sblog_detail' % language_namespace, (), {
            'year': self.entry.pub_date.strftime('%Y'),
            'month': self.entry.pub_date.strftime('%m'),
            'day': self.entry.pub_date.strftime('%d'),
            'slug': self.slug
        })
    get_absolute_url = models.permalink(_get_absolute_url)


        
from cms.models import CMSPlugin

class PygmentsPlugin(CMSPlugin):
    code_language = models.CharField(max_length=20)
    code = models.TextField()
    
class LatestEntriesPlugin(CMSPlugin):
    """
        Model for the settings when using the latest entries cms plugin
    """
    limit = models.PositiveIntegerField(_('Number of entries items to show'), 
                    help_text=_('Limits the number of items that will be displayed'))
                    
    current_language_only = models.BooleanField(_('Only show entries for the current language'))
