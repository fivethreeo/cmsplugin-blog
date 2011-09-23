from simple_translation.middleware import MultilingualGenericsMiddleware, filter_queryset_language
from cmsplugin_blog.models import Entry

class MultilingualBlogEntriesMiddleware(MultilingualGenericsMiddleware):
    
    language_fallback_middlewares = [
        'django.middleware.locale.LocaleMiddleware',
        'cms.middleware.multilingual.MultilingualURLMiddleware'
    ]

    def process_view(self, request, view_func, view_args, view_kwargs):
        super(MultilingualBlogEntriesMiddleware, self).process_view(request, view_func, view_args, view_kwargs)
        if 'queryset_or_model' in view_kwargs and hasattr(view_kwargs['queryset_or_model'], 'model'):
            view_kwargs['queryset_or_model'] = filter_queryset_language(request, view_kwargs['queryset_or_model'])
