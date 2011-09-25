import datetime
try:
    from django.views.generic.dates import BaseDateDetailView, ArchiveIndexView, _date_lookup_for_field, _date_from_string
    from django.views.generic.detail import SingleObjectTemplateResponseMixin
except ImportError:
    from cbv.views.detail import SingleObjectTemplateResponseMixin
    from cbv.views.dates import BaseDateDetailView, ArchiveIndexView, _date_lookup_for_field, _date_from_string

from django.http import Http404
from django.shortcuts import redirect

from cms.middleware.multilingual import has_lang_prefix
from menus.utils import set_language_changer

from simple_translation.middleware import filter_queryset_language
from simple_translation.utils import get_translation_filter, get_translation_filter_language
from cmsplugin_blog.models import Entry
from cmsplugin_blog.utils import is_multilingual

class Redirect(Exception):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        
class DateDetailView(SingleObjectTemplateResponseMixin, BaseDateDetailView):
    # Override to fix django bug
    def get_object(self, queryset=None):
        """
        Get the object this request displays.
        """
        year = self.get_year()
        month = self.get_month()
        day = self.get_day()
        date = _date_from_string(year, self.get_year_format(),
                                 month, self.get_month_format(),
                                 day, self.get_day_format())

        if queryset is None:
            queryset = self.get_queryset()

        if not self.get_allow_future() and date > datetime.date.today(): # pragma: no cover
            raise Http404(_(u"Future %(verbose_name_plural)s not available because %(class_name)s.allow_future is False.") % {
                'verbose_name_plural': queryset.model._meta.verbose_name_plural,
                'class_name': self.__class__.__name__,
            })

        # Filter down a queryset from self.queryset using the date from the
        # URL. This'll get passed as the queryset to DetailView.get_object,
        # which'll handle the 404
        date_field = self.get_date_field()
        field = queryset.model._meta.get_field(date_field)
        lookup = _date_lookup_for_field(field, date)
        queryset = queryset.filter(**lookup)

        return super(BaseDateDetailView, self).get_object(queryset=queryset)
    
class EntryDateDetailView(DateDetailView):
    slug_field = get_translation_filter(Entry, slug=None).items()[0][0]
    date_field = 'pub_date'
    template_name_field = 'template'
    month_format = '%m'
    queryset = Entry.objects.all()
    
    def get_object(self):
        try:
            obj = super(EntryDateDetailView, self).get_object()
        except Http404, e:
            # No entry has been found for a given language, we fallback to search for an entry in any language
            # Could find multiple entries, in this way we cannot decide which one is the right one, so we let
            # exception be propagated FIXME later
            if is_multilingual():
                try:
                    queryset = self.get_unfiltered_queryset()
                    obj = super(EntryDateDetailView, self).get_object(queryset=queryset)
                except Entry.MultipleObjectsReturned, s:
                    raise e
                # We know there is only one title for this entry, so we can simply use get()
                raise Redirect(obj.entrytitle_set.get().get_absolute_url())

        set_language_changer(self.request, obj.language_changer)
        return obj
        
    def get_unfiltered_queryset(self):
        return super(EntryDateDetailView, self).get_queryset().published()
            
    def get_queryset(self):
        queryset = super(EntryDateDetailView, self).get_queryset()
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
