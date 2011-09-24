from django.contrib.sites.models import get_current_site
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms import settings
from cms.utils import get_language_from_request
from simple_translation.translation_pool import translation_pool
from simple_translation.templatetags.simple_translation_tags import get_preferred_translation_from_lang
from simple_translation.utils import get_translation_filter, get_translation_filter_language

from cmsplugin_blog.models import Entry
from cmsplugin_blog.utils import is_multilingual, get_lang_name, add_current_root

class EntriesFeed(Feed):
    title_template = "cmsplugin_blog/feed_entries_title.html"
    description_template = "cmsplugin_blog/feed_entries_description.html"

    def get_object(self, request, **kwargs):
        self.language_code = get_language_from_request(request)
        self.site = get_current_site(request)
        self.any_language = kwargs.get('any_language', None)
        self.language_namespace = ''
        if is_multilingual():
            self.language_namespace = '%s:' % self.language_code
        return None
    
    def feed_url(self, obj):
        if self.any_language:
            return add_current_root(reverse('%sblog_rss_any' % self.language_namespace))
        return add_current_root(reverse('%sblog_rss' % self.language_namespace))
        
    def title(self, obj):
        if self.any_language or not is_multilingual():
            return _(u"%(site)s blog entries") % {'site': self.site.name}
        return _(u"%(site)s blog entries in %(lang)s") % {'site': self.site.name, 'lang': get_lang_name(self.language_code)}

    def link(self, obj):
        return add_current_root(reverse('%sblog_archive_index' % self.language_namespace))

    def item_link(self, obj):
        return add_current_root(obj.get_absolute_url())

    def description(self, obj):
        if self.any_language or not is_multilingual():
            return _(u"%(site)s blog entries") % {'site': self.site.name}
        return _(u"%(site)s blog entries in %(lang)s") % {'site': self.site.name, 'lang': get_lang_name(self.language_code)}

    def get_queryset(self, obj):
        if not is_multilingual() or self.any_language :
            qs = Entry.published.order_by('-pub_date')
        else:
            kw = get_translation_filter_language(Entry, self.language_code)
            qs = Entry.published.filter(**kw).order_by('-pub_date').distinct()
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
        return Entry.tagged.with_any(self.tag, queryset=qs).distinct()
        
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
        kw = get_translation_filter(Entry, **{'author__username': self.author})
        return qs.filter(**kw).distinct()
