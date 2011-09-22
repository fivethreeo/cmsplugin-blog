from simple_translation.middleware import MultilingualGenericsMiddleware
from cmsplugin_blog.models import Entry

class MultilingualBlogEntriesMiddleware(MultilingualGenericsMiddleware):
    
    language_fallback_middlewares = [
        'django.middleware.locale.LocaleMiddleware',
        'cms.middleware.multilingual.MultilingualURLMiddleware'
    ]