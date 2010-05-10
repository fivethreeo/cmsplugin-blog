from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.translation import get_language

from cms import settings
from cms.utils import get_language_from_request
from cms.middleware.multilingual import has_lang_prefix
from simple_translation.translation_pool import translation_pool
from simple_translation.templatetags.simple_translation_tags import get_preferred_translation_from_lang

def get_lang_name(lang):
    return dict(settings.LANGUAGES)[lang]
    
def add_current_root(url):
    if not has_lang_prefix(url):
        new_root = "/%s" % get_language()
        url = new_root + url
    return url

class EntriesFeed(Feed):
    
    def get_object(self, request, **kwargs):
        self.language_code = get_language_from_request(request)        
        self.any_language = kwargs.get('any_language', None)
        return None
    
    def feed_url(self, obj):
        if self.any_language:
            return add_current_root(reverse('%s:blog_rss_any' % self.language_code))
        return add_current_root(reverse('%s:blog_rss' % self.language_code))
        
    def title(self, obj):
        if self.any_language:
            return "Blog entries"
        return "Blog entries in %s" % get_lang_name(self.language_code)

    def link(self, obj):
        return add_current_root(reverse('%s:blog_archive_index' % self.language_code))

    def item_link(self, obj):
        return add_current_root(obj.get_absolute_url())

    def description(self, obj):        
        if self.any_language:
            return "Blog entries"
        return "Blog entries in %s" % get_lang_name(self.language_code)

    def items(self, obj):
        from cmsplugin_blog.models import Entry
        if self.any_language:
            items = Entry.objects.order_by('-pub_date')[:10]
        else:
            items = Entry.objects.filter(entrytitle__language=self.language_code).order_by('-pub_date')[:10]
        
        items = [get_preferred_translation_from_lang(title, self.language_code) for title in translation_pool.annotate_with_translations(items)]
        return items
