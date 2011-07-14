try:
    from django.views.generic import DateDetailView
except ImportError:
    from cbv import DateDetailView

from menus.utils import set_language_changer
from cmsplugin_blog.models import Entry

class PublishedPreviewMixin(object):

    def get_queryset(self):
        queryset = super(PublishedPreviewMixin, self).get_queryset()
        if request.user.is_staff:
            return queryset
        else:
            return queryset.published()
            
class EntryDateDetailView(DateDetailView, PublishedPreviewMixin):
    
    month_format = '%m'
    queryset = Entry.objects.all()
    
    def get_object(self):
        obj = super(EntryDateDetailView, self).get_object()
        set_language_changer(self.request, self.object.get_absolute_url)
        return obj

