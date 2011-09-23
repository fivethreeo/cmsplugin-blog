try:
    from django.views.generic import DateDetailView, ArchiveIndexView
except ImportError:
    from cbv import DateDetailView, ArchiveIndexView

from django.http import Http404
from django.shortcuts import redirect

from menus.utils import set_language_changer

from simple_translation.middleware import filter_queryset_language
from simple_translation.utils import get_translation_filter
from cmsplugin_blog.models import Entry

class Redirect(Exception):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

class EntryDateDetailView(DateDetailView):
    slug_field = get_translation_filter(Entry, slug=None).items()[0][0]
    date_field = 'pub_date'
    template_name_field = 'template'
    month_format = '%m'
    queryset = Entry.objects.all()

    def __init__(self, *args, **kwargs):
        # Ugly hack because of https://code.djangoproject.com/ticket/16918
        # Otherwise we could simply provide a queryset to get_object
        self._should_get_queryset_limit_language = True
    
    def get_object(self):
        try:
            obj = super(EntryDateDetailView, self).get_object()
        except Http404, e:
            # No entry has been found for a given language, we fallback to search for an entry in any language
            # Could find multiple entries, in this way we cannot decide which one is the right one, so we let
            # exception be propagated
            self._should_get_queryset_limit_language = False
            try:
                obj = super(EntryDateDetailView, self).get_object()
            except Entry.MultipleObjectsReturned:
                raise e
            # We know there is only one title for this entry, so we can simply use get()
            raise Redirect(obj.entrytitle_set.get().get_absolute_url())
        finally:
            self._should_get_queryset_limit_language = True
        set_language_changer(self.request, obj.language_changer)
        return obj
        
    def get_queryset(self):
        queryset = super(EntryDateDetailView, self).get_queryset()
        if self._should_get_queryset_limit_language:
            queryset = filter_queryset_language(self.request, queryset)
        if self.request.user.is_staff or self.request.user.is_superuser:
            return queryset
        else:
            return queryset.published()

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(EntryDateDetailView, self).dispatch(request, *args, **kwargs)
        except Redirect, e:
            return redirect(*e.args, **e.kwargs)

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
