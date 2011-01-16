import datetime
from django.core.urlresolvers import reverse
from cmsplugin_blog.test.testcases import BaseBlogTestCase

from django.contrib.auth.models import User

class BlogTestCase(BaseBlogTestCase):
    
    def test_01_apphook_added(self):
        self.assertEquals(reverse('en:blog_archive_index'), '/en/test-page-1/')
        self.assertEquals(reverse('de:blog_archive_index'), '/de/test-page-1/')
        
    def test_02_title_absolute_url(self):
        published_at = datetime.datetime.now() - datetime.timedelta(hours=-1)
        title, entry = self.create_entry_with_title(published=True, 
            published_at=published_at)
        self.assertEquals(title.get_absolute_url(), '/en/test-page-1/%s/entry-title/' % published_at.strftime('%Y/%m/%d'))

    def test_03_admin_change(self):
        
        superuser = User(username="super", is_staff=True, is_active=True, 
            is_superuser=True)
        superuser.set_password("super")
        superuser.save()
        
        self.client.login(username='super', password='super')
        
        published_at = datetime.datetime.now() - datetime.timedelta(hours=-1)
        en_title, entry = self.create_entry_with_title(title='english', published_at=published_at)
        
        de_title = self.create_entry_title(entry, title='german', language='de')
        
        edit_url = reverse('admin:cmsplugin_blog_entry_change', args=(str(entry.pk)))
        
        # edit english
        response = self.client.get(edit_url, {'language': 'en'})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'language_button selected" id="debutton" name="en"' )
        
        # edit german
        response = self.client.get(edit_url, {'language': 'de'})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'language_button selected" id="debutton" name="de"' )