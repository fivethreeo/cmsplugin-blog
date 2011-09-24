from django.utils.translation import get_language, ugettext_lazy as _
from cms import settings
from cms.middleware.multilingual import has_lang_prefix

def is_multilingual():
    return 'cmsplugin_blog.middleware.MultilingualBlogEntriesMiddleware' in settings.MIDDLEWARE_CLASSES

def get_lang_name(lang):
    return _(dict(settings.LANGUAGES)[lang])

def add_current_root(url):
    if is_multilingual() and not has_lang_prefix(url):
        new_root = "/%s" % get_language()
        url = new_root + url
    return url
