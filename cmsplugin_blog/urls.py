from django.conf.urls.defaults import *
from cmsplugin_blog.models import Entry

blog_info_dict = {
    'queryset': Entry.published.all(),
    'date_field': 'pub_date',
}

blog_info_month_dict = {
    'queryset': Entry.published.all(),
    'date_field': 'pub_date',
    'month_format': '%m',
}

blog_info_detail_dict = dict(blog_info_month_dict, slug_field='entrytitle__slug')

def feed(request, **kwargs):
    from cms.utils import get_language_from_request
    from cmsplugin_blog.feeds import EntriesFeed
    return EntriesFeed()(request, language_code=get_language_from_request(request), **kwargs)

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

    (r'^rss/any/$', feed, {'any_language': True}, 'blog_rss_any'),
    (r'^rss/$', feed, {}, 'blog_rss')
)
