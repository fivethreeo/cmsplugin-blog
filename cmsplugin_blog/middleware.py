from cms.utils import get_language_from_request
from cmsplugin_blog.models import Entry

class MultilingualBlogEntriesMiddleware:

    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'queryset' in view_kwargs and view_kwargs['queryset'].model == Entry:
            view_kwargs['queryset'] = view_kwargs['queryset'].filter(language=language)
            

