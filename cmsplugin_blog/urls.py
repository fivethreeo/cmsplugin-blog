from cmsplugin_blog.feeds import EntriesFeed, TaggedEntriesFeed
from cmsplugin_blog.models import Entry
from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.date_based import archive_index, archive_year, archive_month, archive_day, object_detail
from tagging.views import tagged_object_list

blog_info_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'pub_date',
}

blog_info_tagged_dict = {
    'queryset_or_model': Entry.objects.all(),
}

blog_info_month_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'pub_date',
    'month_format': '%m',
}

blog_info_detail_dict = dict(blog_info_month_dict, slug_field='entrytitle__slug')

def blog_archive_index(request, **kwargs):
    kwargs['queryset'] = kwargs['queryset'].published()
    return archive_index(request, **kwargs)
    
def blog_archive_year(request, **kwargs):
    kwargs['queryset'] = kwargs['queryset'].published()
    return archive_year(request, **kwargs)
    
def blog_archive_month(request, **kwargs):
    kwargs['queryset'] = kwargs['queryset'].published()
    return archive_month(request, **kwargs)

def blog_archive_day(request, **kwargs):
    kwargs['queryset'] = kwargs['queryset'].published()
    return archive_day(request, **kwargs)

def blog_detail(request, **kwargs):
    kwargs['queryset'] = kwargs['queryset'].published()
    return object_detail(request, **kwargs)
    
def blog_archive_tagged(request, **kwargs):
    kwargs['queryset_or_model'] = kwargs['queryset_or_model'].published()
    return tagged_object_list(request, **kwargs)


urlpatterns = patterns('',
    (r'^$', blog_archive_index, blog_info_dict, 'blog_archive_index'),
    
    (r'^(?P<year>\d{4})/$', 
        blog_archive_year, blog_info_dict, 'blog_archive_year'),
    
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 
        blog_archive_month, blog_info_month_dict, 'blog_archive_month'),
    
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 
        blog_archive_day, blog_info_month_dict, 'blog_archive_day'),
    
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 
        blog_detail, blog_info_detail_dict, 'blog_detail'),
        
    (r'^tagged/(?P<tag>[^/]*)/$', blog_archive_tagged, blog_info_tagged_dict, 'blog_archive_tagged'),
    
    (r'^rss/any/tagged/(?P<tag>[^/]*)/$', TaggedEntriesFeed(), {'any_language': True}, 'blog_rss_any_tagged'),
    
    (r'^rss/tagged/(?P<tag>[^/]*)/$', TaggedEntriesFeed(), {}, 'blog_rss_tagged'),
    
    (r'^rss/any/$', EntriesFeed(), {'any_language': True}, 'blog_rss_any'),
    
    (r'^rss/$', EntriesFeed(), {}, 'blog_rss')
    
)
