from django.contrib.sitemaps import Sitemap
from cmsplugin_blog.models import EntryTitle

class BlogSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return EntryTitle.objects.filter(entry__is_published=True)

    def lastmod(self, obj):
        return obj.entry.pub_date