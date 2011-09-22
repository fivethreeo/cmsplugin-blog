from django.conf import settings
from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from django.views.generic.date_based import archive_year, archive_month, archive_day, object_detail
from django.views.generic.list_detail import object_list

from tagging.views import tagged_object_list

from menus.utils import set_language_changer

from cms.models import Title
from cms.utils.urlutils import urljoin

from cmsplugin_blog.feeds import EntriesFeed, TaggedEntriesFeed, AuthorEntriesFeed
from cmsplugin_blog.models import Entry
from cmsplugin_blog.views import EntryDateDetailView, EntryArchiveIndexView

blog_info_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'pub_date',
    'allow_empty': True,
    'paginate_by': 15,
}

blog_info_tagged_dict = {
    'queryset_or_model': Entry.objects.all(),
    'allow_empty': True,
}

blog_info_author_dict = {
    'queryset': Entry.objects.all(),
    'allow_empty': True,
    'template_name': 'cmsplugin_blog/entry_author_list.html',
}

blog_info_month_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'pub_date',
    'month_format': '%m',
    'allow_empty': True,
}

blog_info_year_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'pub_date',
    'make_object_list': True,
    'allow_empty': True,
}

blog_info_detail_dict = dict(blog_info_month_dict, slug_field='entrytitle__slug')

def language_changer(lang):
    request = language_changer.request
    return request.get_full_path()

blog_archive_index = EntryArchiveIndexView.as_view()

def blog_archive_year(request, **kwargs):
    kwargs['queryset'] = kwargs['queryset'].published()
    set_language_changer(request, language_changer)
    return archive_year(request, **kwargs)
    
def blog_archive_month(request, **kwargs):
    kwargs['queryset'] = kwargs['queryset'].published()
    set_language_changer(request, language_changer)
    return archive_month(request, **kwargs)

def blog_archive_day(request, **kwargs):
    kwargs['queryset'] = kwargs['queryset'].published()
    set_language_changer(request, language_changer)
    return archive_day(request, **kwargs)

blog_detail = EntryDateDetailView.as_view()

def blog_archive_tagged(request, **kwargs):
    kwargs['queryset_or_model'] = kwargs['queryset_or_model'].published()
    set_language_changer(request, language_changer)
    return tagged_object_list(request, **kwargs)

def blog_archive_author(request, **kwargs):
    author = kwargs.pop('author')
    kwargs['queryset'] = kwargs['queryset'].published().filter(entrytitle__author__username=author)
    kwargs['extra_context'] = {
        'author': author,
    }
    set_language_changer(request, language_changer)
    return object_list(request, **kwargs)

urlpatterns = patterns('',
    (r'^$', blog_archive_index, blog_info_dict, 'blog_archive_index'),
    
    (r'^(?P<year>\d{4})/$', 
        blog_archive_year, blog_info_year_dict, 'blog_archive_year'),
    
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 
        blog_archive_month, blog_info_month_dict, 'blog_archive_month'),
    
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 
        blog_archive_day, blog_info_month_dict, 'blog_archive_day'),
    
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 
        blog_detail, blog_info_detail_dict, 'blog_detail'),
        
    (r'^tagged/(?P<tag>[^/]*)/$', blog_archive_tagged, blog_info_tagged_dict, 'blog_archive_tagged'),

    (r'^author/(?P<author>[^/]*)/$', blog_archive_author, blog_info_author_dict, 'blog_archive_author'),
    
    (r'^rss/any/tagged/(?P<tag>[^/]*)/$', TaggedEntriesFeed(), {'any_language': True}, 'blog_rss_any_tagged'),
    
    (r'^rss/tagged/(?P<tag>[^/]*)/$', TaggedEntriesFeed(), {}, 'blog_rss_tagged'),
    
    (r'^rss/any/author/(?P<author>[^/]*)/$', AuthorEntriesFeed(), {'any_language': True}, 'blog_rss_any_author'),
    
    (r'^rss/author/(?P<author>[^/]*)/$', AuthorEntriesFeed(), {}, 'blog_rss_author'),
    
    (r'^rss/any/$', EntriesFeed(), {'any_language': True}, 'blog_rss_any'),
    
    (r'^rss/$', EntriesFeed(), {}, 'blog_rss')
    
)
