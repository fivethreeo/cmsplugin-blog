from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.translation import get_language, ugettext_lazy as _

from cms import settings
from cms.utils import get_language_from_request
from cms.middleware.multilingual import has_lang_prefix
from simple_translation.translation_pool import translation_pool
from simple_translation.templatetags.simple_translation_tags import get_preferred_translation_from_lang

from cmsplugin_blog.models import Entry

def get_lang_name(lang):
    return _(dict(settings.LANGUAGES)[lang])
    
def add_current_root(url):
    if not has_lang_prefix(url):
        new_root = "/%s" % get_language()
        url = new_root + url
    return url

class EntriesFeed(Feed):
    title_template = "cmsplugin_blog/feed_entries_title.html"
    description_template = "cmsplugin_blog/feed_entries_description.html"

    def get_object(self, request, **kwargs):
        self.language_code = get_language_from_request(request)
        self.any_language = kwargs.get('any_language', None)
        self.language_namespace = ''
        if 'cmsplugin_blog.middleware.MultilingualBlogEntriesMiddleware' in settings.MIDDLEWARE_CLASSES:
            self.language_namespace = '%s:' % self.language_code
        else:
            self.any_language = True
        return None
    
    def feed_url(self, obj):
        if self.any_language:
            return add_current_root(reverse('%sblog_rss_any' % self.language_namespace))
        return add_current_root(reverse('%sblog_rss' % self.language_namespace))
        
    def title(self, obj):
        if self.any_language:
            return _(u"Blog entries")
        return _(u"Blog entries in %s") % get_lang_name(self.language_code)

    def link(self, obj):
        return add_current_root(reverse('%sblog_archive_index' % self.language_namespace))

    def item_link(self, obj):
        return add_current_root(obj.get_absolute_url())

    def description(self, obj):        
        if self.any_language:
            return _(u"Blog entries")
        return _(u"Blog entries in %s") % get_lang_name(self.language_code)

    def get_queryset(self, obj):
        if self.any_language:
            qs = Entry.published.order_by('-pub_date')
        else:
            qs = Entry.published.filter(entrytitle__language=self.language_code).order_by('-pub_date')
        return qs
        
    def items(self, obj):
        items = self.get_queryset(obj)[:10]
        items = [get_preferred_translation_from_lang(title, self.language_code) for title in translation_pool.annotate_with_translations(items)]
        return items
        
    def item_pubdate(self, item):
        return item.entry.pub_date

class TaggedEntriesFeed(EntriesFeed):
    title_template = "cmsplugin_blog/feed_tagged_title.html"
    description_template = "cmsplugin_blog/feed_tagged_description.html"
    
    def get_object(self, request, **kwargs):
        super(TaggedEntriesFeed, self).get_object(request, **kwargs)
        self.tag = kwargs.get('tag')
        return None
    
    def title(self, obj):
        title = super(TaggedEntriesFeed, self).title(obj)
        return _(u'%(title)s tagged "%(tag)s"') % {'title': title, 'tag': self.tag}
        
    def feed_url(self, obj):
        if self.any_language:
            return add_current_root(reverse('%sblog_rss_any_tagged' % self.language_namespace, kwargs={'tag': self.tag}))
        return add_current_root(reverse('%sblog_rss_tagged' % self.language_namespace, kwargs={'tag': self.tag}))
        
    def link(self, obj):
        return add_current_root(reverse('%sblog_archive_tagged' % self.language_namespace, kwargs={'tag': self.tag}))

    def description(self, obj):
        description = super(TaggedEntriesFeed, self).description(obj)
        return _(u'%(description)s tagged "%(tag)s"') % {'description': description, 'tag': self.tag}
        
    def get_queryset(self, obj):
        qs = super(TaggedEntriesFeed, self).get_queryset(obj)
        return Entry.tagged.with_any(self.tag, queryset=qs)
        
class AuthorEntriesFeed(EntriesFeed):
    title_template = "cmsplugin_blog/feed_author_title.html"
    description_template = "cmsplugin_blog/feed_author_description.html"

    def get_object(self, request, **kwargs):
        super(AuthorEntriesFeed, self).get_object(request, **kwargs)
        self.author = kwargs.get('author')
        return None
    
    def title(self, obj):
        title = super(AuthorEntriesFeed, self).title(obj)
        return _(u'%(title)s by %(author)s') % {'title': title, 'author': self.author}
    
    def feed_url(self, obj):
        if self.any_language:
            return add_current_root(reverse('%sblog_rss_any_author' % self.language_namespace, kwargs={'author': self.author}))
        return add_current_root(reverse('%sblog_rss_author' % self.language_namespace, kwargs={'author': self.author}))
    
    def link(self, obj):
        return add_current_root(reverse('%sblog_archive_author' % self.language_namespace, kwargs={'author': self.author}))
    
    def description(self, obj):
        description = super(AuthorEntriesFeed, self).description(obj)
        return _(u'%(description)s by %(author)s') % {'description': description, 'author': self.author}
    
    def get_queryset(self, obj):
        qs = super(AuthorEntriesFeed, self).get_queryset(obj)
        return qs.filter(entrytitle__author__username=self.author)
