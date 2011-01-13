import datetime
from django.core.urlresolvers import reverse
from cmsplugin_blog.test.testcases import BaseBlogTestCase

class BlogTestCase(BaseBlogTestCase):
    
    def test_01_apphook_added(self):
        self.assertEquals(reverse('en:blog_archive_index'), '/en/test-page-1/')
        self.assertEquals(reverse('de:blog_archive_index'), '/de/test-page-1/')
        
    def test_02_title_absolute_url(self):
        published_at = datetime.datetime.now() - datetime.timedelta(hours=-1)
        title, entry = self.create_entry_with_title(published=True, 
            published_at=published_at)
        self.assertEquals(title.get_absolute_url(), '/en/test-page-1/%s/entry-title/' % published_at.strftime('%Y/%m/%d'))
