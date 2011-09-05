try:
    from django.views.generic import DateDetailView
except ImportError:
    from cbv import DateDetailView
    
from menus.utils import set_language_changer

from simple_translation.utils import get_translation_filter
from cmsplugin_blog.models import Entry

class EntryDateDetailView(DateDetailView):
    
    slug_field = get_translation_filter(Entry, slug=None).items()[0][0]
    date_field = 'pub_date'
    template_name_field = 'template'
    month_format = '%m'
    queryset = Entry.objects.all()
    
    def get_object(self):
        obj = super(EntryDateDetailView, self).get_object()
        set_language_changer(self.request, obj.language_changer)
        return obj
        
    def get_queryset(self):
        queryset = super(EntryDateDetailView, self).get_queryset()
        if self.request.user.is_staff or self.request.user.is_superuser:
            return queryset
        else:
            return queryset.published()
