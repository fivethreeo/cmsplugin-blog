from django.utils.translation import ugettext_lazy as _

from django.db import models
from cms.models.fields import PlaceholderField
import datetime

from django.conf import settings

import tagging
from tagging.fields import TagField

if "south" in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    rules = [
        (
            (TagField, ),
            [],
            {
                "blank": ["blank", {"default": True}],
                "max_length": ["max_length", {"default": 255}],
            },
        ),
    ]
    
    add_introspection_rules(rules, ["^tagging_autocomplete\.models",])


class PublishedEntriesManager(models.Manager):
    """
        Filters out all unpublished and items with a publication date in the future
    """
    def get_query_set(self):
        return super(PublishedEntriesManager, self).get_query_set() \
                    .filter(is_published=True, pub_date__lte=datetime.datetime.now())
                    
class Entry(models.Model):
    is_published = models.BooleanField(_('Is published'))
    content = PlaceholderField('entry', verbose_name=_('Content'))
    pub_date = models.DateTimeField(_('Published'), default=datetime.datetime.now)
 
    tags = TagField()
    
    objects = models.Manager()
    published = PublishedEntriesManager()
    
    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')
        ordering = ('-pub_date', )

tagging.register(Entry, tag_descriptor_attr='entry_tags')

class EntryTitle(models.Model):
    entry = models.ForeignKey(Entry, verbose_name=_('Entry'))
    language = models.CharField(_('Language'), max_length=2, choices=settings.LANGUAGES)
    title = models.CharField(_('Title'), max_length=255)
    slug = models.SlugField(_('Slug'))
    
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

    class Meta:
        verbose_name = _('Entry title')
        verbose_name_plural = _('Entry titles')
        
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
