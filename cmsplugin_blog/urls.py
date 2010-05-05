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

urlpatterns = patterns('django.views.generic.date_based',
    (r'^$', 
        'archive_index', blog_info_dict, 'blog_archive_index'),
    
    (r'^(?P<year>\d{4})/$', 
        'archive_year', blog_info_dict, 'blog_archive_year'),
    
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 
        'archive_month', blog_info_month_dict, 'blog_archive_month'),
    
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 
        'archive_day', blog_info_month_dict, 'blog_archive_day'),
    
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 
        'object_detail', dict(blog_info_month_dict, slug_field='entrytitle__slug'), 'blog_detail'),
)

