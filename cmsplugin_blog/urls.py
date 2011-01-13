from cmsplugin_blog.feeds import EntriesFeed, TaggedEntriesFeed
from cmsplugin_blog.models import Entry
from django.conf import settings
from django.conf.urls.defaults import *

blog_info_dict = {
    'queryset': Entry.published.all(),
    'date_field': 'pub_date',
}

blog_info_tagged_dict = {
    'queryset_or_model': Entry.published.all(),
}

blog_info_month_dict = {
    'queryset': Entry.published.all(),
    'date_field': 'pub_date',
    'month_format': '%m',
}

blog_info_detail_dict = dict(blog_info_month_dict, slug_field='entrytitle__slug')

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.date_based.archive_index', blog_info_dict, 'blog_archive_index'),
    
    (r'^(?P<year>\d{4})/$', 
        'django.views.generic.date_based.archive_year', blog_info_dict, 'blog_archive_year'),
    
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 
        'django.views.generic.date_based.archive_month', blog_info_month_dict, 'blog_archive_month'),
    
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 
        'django.views.generic.date_based.archive_day', blog_info_month_dict, 'blog_archive_day'),
    
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 
        'django.views.generic.date_based.object_detail', blog_info_detail_dict, 'blog_detail'),
        
    (r'^tagged/(?P<tag>[^/]*)/$', 'tagging.views.tagged_object_list', blog_info_tagged_dict, 'blog_archive_tagged'),
    
    (r'^rss/any/tagged/(?P<tag>[^/]*)/$', TaggedEntriesFeed(), {'any_language': True}, 'blog_rss_any_tagged'),
    
    (r'^rss/tagged/(?P<tag>[^/]*)/$', TaggedEntriesFeed(), {}, 'blog_rss_tagged'),
    
    (r'^rss/any/$', EntriesFeed(), {'any_language': True}, 'blog_rss_any'),
    
    (r'^rss/$', EntriesFeed(), {}, 'blog_rss')
    
)
