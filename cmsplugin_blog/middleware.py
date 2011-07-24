from simple_translation.middleware import MultilingualGenericsMiddleware
from cmsplugin_blog.models import Entry

class MultilingualBlogEntriesMiddleware(MultilingualGenericsMiddleware):
    
    language_fallback_middlewares = [
        'django.middleware.locale.LocaleMiddleware',
        'cms.middleware.multilingual.MultilingualURLMiddleware'
    ]

    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'queryset' in view_kwargs and view_kwargs['queryset'].model == Entry:
            super(MultilingualBlogEntriesMiddleware, self).process_view(
                request, view_func, view_args, view_kwargs)
        if 'queryset_or_model' in view_kwargs and getattr(view_kwargs['queryset_or_model'], 'model', None) == Entry:
            view_kwargs['queryset'] = view_kwargs['queryset_or_model']
            super(MultilingualBlogEntriesMiddleware, self).process_view(
                request, view_func, view_args, view_kwargs)
            view_kwargs['queryset_or_model'] = view_kwargs['queryset']
            del view_kwargs['queryset'] 
