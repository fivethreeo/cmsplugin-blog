try:
    from django.views.generic import DateDetailView
except ImportError:
    from cbv import DateDetailView

from menus.utils import set_language_changer
from cmsplugin_blog.models import Entry
            
class EntryDateDetailView(DateDetailView):
    
    slug_field = 'entrytitle__slug'
    date_field = 'pub_date'
    month_format = '%m'
    queryset = Entry.objects.all()
    
    def get_object(self):
        obj = super(EntryDateDetailView, self).get_object()
        set_language_changer(self.request, obj.get_absolute_url)
        return obj
        
    def get_queryset(self):
        queryset = super(EntryDateDetailView, self).get_queryset()
        if self.request.user.is_staff:
            return queryset
        else:
            return queryset.published()
