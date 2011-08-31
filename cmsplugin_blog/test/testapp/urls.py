from django.conf.urls.defaults import *
from django.contrib import admin
from cmsplugin_blog.sitemaps import BlogSitemap

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),
)


urlpatterns += patterns('',
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {
        'sitemaps': {
            'blogentries': BlogSitemap
        }
    }),
    url(r'^', include('cms.urls'))
)
