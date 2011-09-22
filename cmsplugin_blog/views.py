try:
    from django.views.generic import DateDetailView, ArchiveIndexView
except ImportError:
    from cbv import DateDetailView, ArchiveIndexView
    
from menus.utils import set_language_changer

from simple_translation.middleware import filter_queryset_language
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
        queryset = filter_queryset_language(self.request, queryset)
        if self.request.user.is_staff or self.request.user.is_superuser:
            return queryset
        else:
            return queryset.published()

class EntryArchiveIndexView(ArchiveIndexView):
    date_field = 'pub_date'
    allow_empty = True
    paginate_by = 15
    template_name_field = 'template'
    queryset = Entry.objects.all()

    def get_dated_items(self):
        items = super(EntryArchiveIndexView, self).get_dated_items()
        from cmsplugin_blog.urls import language_changer
        set_language_changer(self.request, language_changer)
        return items

    def get_dated_queryset(self, **lookup):
        queryset = super(EntryArchiveIndexView, self).get_dated_queryset(**lookup)
        queryset = filter_queryset_language(self.request, queryset)
        return queryset.published()
