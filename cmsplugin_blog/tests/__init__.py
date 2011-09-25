from __future__ import with_statement
import datetime
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import Http404
from django.db import connection
from cms.models.placeholdermodel import Placeholder

from cmsplugin_blog.models import Entry, LatestEntriesPlugin
from cmsplugin_blog.test.testcases import BaseBlogTestCase

class NULL:
    pass
    
class SettingsOverride(object):
    """
    Overrides Django settings within a context and resets them to their inital
    values on exit.
    Example:
    with SettingsOverride(DEBUG=True):
    # do something
    """
    
    def __init__(self, **overrides):
        self.overrides = overrides
        
    def __enter__(self):
        self.old = {}
        for key, value in self.overrides.items():
            self.old[key] = getattr(settings, key, NULL)
            setattr(settings, key, value)
        
    def __exit__(self, type, value, traceback):
        for key, value in self.old.items():
            if value is not NULL:
                setattr(settings, key, value)
            else:
                delattr(settings,key) # do not pollute the context!
                
class BlogTestCase(BaseBlogTestCase):
    
    def test_01_apphook_added(self):
        self.assertEquals(reverse('en:blog_archive_index'), '/test-page-1/')
        self.assertEquals(reverse('de:blog_archive_index'), '/de/test-page-1/')
        
    def test_02_title_absolute_url(self):
        published_at = datetime.datetime.now() - datetime.timedelta(hours=1)
        title, entry = self.create_entry_with_title(published=True, 
            published_at=published_at)
        self.assertEquals(title.get_absolute_url(), '/test-page-1/%s/entry-title/' % published_at.strftime('%Y/%m/%d'))
        
    def test_03_admin_add(self):
        
        superuser = User(username="super", is_staff=True, is_active=True, 
            is_superuser=True)
        superuser.set_password("super")
        superuser.save()
        
        self.client.login(username='super', password='super')
        
        add_url = reverse('admin:cmsplugin_blog_entry_add')
        
        # edit english
        response = self.client.get(add_url, {'language': 'en'})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'value="English" type="button" disabled' )
        
        # edit german
        response = self.client.get(add_url, {'language': 'de'})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'value="German" type="button" disabled')
        
    def test_04_admin_change(self):
        
        superuser = User(username="super", is_staff=True, is_active=True, 
            is_superuser=True)
        superuser.set_password("super")
        superuser.save()
        
        self.client.login(username='super', password='super')
        
        published_at = datetime.datetime.now() - datetime.timedelta(hours=1)
        en_title, entry = self.create_entry_with_title(title='english', published_at=published_at)
        
        de_title = self.create_entry_title(entry, title='german', language='de')
        
        edit_url = reverse('admin:cmsplugin_blog_entry_change', args=(str(entry.pk)))
        
        # edit english
        response = self.client.get(edit_url, {'language': 'en'})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'value="English" type="button" disabled' )

        
        # edit german
        response = self.client.get(edit_url, {'language': 'de'})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'value="German" type="button" disabled' )

    def test_05_admin_add_post(self):
        
        superuser = User(username="super", is_staff=True, is_active=True, 
            is_superuser=True)
        superuser.set_password("super")
        superuser.save()
        
        self.client.login(username='super', password='super')
        
        add_url = reverse('admin:cmsplugin_blog_entry_add')
        
        # add english
        response = self.client.post(add_url, {'language': 'en', 'title': 'english', 'slug': 'english',
            'pub_date_0': '2011-01-16', 'pub_date_1': '09:09:09', 'author': '1'})
        # self.assertEquals(response.content, '')

        self.assertEquals(response.status_code, 302)
        
        edit_url = reverse('admin:cmsplugin_blog_entry_change', args=(1,))

        # add german
        response = self.client.post(edit_url, {'language': 'de', 'title': 'german', 'slug': 'german',
            'pub_date_0': '2011-01-16', 'pub_date_1': '09:09:09'})
        self.assertEquals(response.status_code, 302)
        
        entry = Entry.objects.get(pk=1)
        self.assertEquals([title.title for title in entry.entrytitle_set.all()], ['english', 'german'])
        
    def test_06_admin_changelist(self):
        
        published_at = datetime.datetime.now() - datetime.timedelta(hours=1)
        title, entry = self.create_entry_with_title(published=True, 
            published_at=published_at)
                    
        superuser = User(username="super", is_staff=True, is_active=True, 
            is_superuser=True)
        superuser.set_password("super")
        superuser.save()
        
        self.client.login(username='super', password='super')
        
        changelist_url = reverse('admin:cmsplugin_blog_entry_changelist')
        response = self.client.get(changelist_url)
        self.assertEquals(response.status_code, 200)
                
class BlogRSSTestCase(BaseBlogTestCase):
    
    def test_01_posts_one_language(self):
        published_at = datetime.datetime.now() - datetime.timedelta(hours=1)
        title, entry = self.create_entry_with_title(published=True, 
            published_at=published_at)
        response = self.client.get(reverse('en:blog_rss'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'in English')
        
    def test_02_posts_all_languages(self):
        published_at = datetime.datetime.now() - datetime.timedelta(hours=1)
        title, entry = self.create_entry_with_title(published=True, 
            published_at=published_at)
        response = self.client.get(reverse('en:blog_rss_any'))
        self.assertEquals(response.status_code, 200)
        self.assertNotContains(response, 'in English')
        
    def test_03_posts_by_author_single_language(self):
        user = User.objects.all()[0]
        published_at = datetime.datetime.now() - datetime.timedelta(hours=1)
        title, entry = self.create_entry_with_title(published=True, 
            published_at=published_at, author=user)
        response = self.client.get(reverse('en:blog_rss_author', kwargs={'author': user.username}))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'in English')  
        
    def test_04_posts_by_author_all_languages(self):
        user = User.objects.all()[0]
        published_at = datetime.datetime.now() - datetime.timedelta(hours=1)
        title, entry = self.create_entry_with_title(published=True, 
            published_at=published_at, author=user)
        response = self.client.get(reverse('en:blog_rss_any_author', kwargs={'author': user.username}))
        self.assertEquals(response.status_code, 200)
        self.assertNotContains(response, 'in English')
        
    def test_05_posts_tagged_single_language(self):
        published_at = datetime.datetime.now() - datetime.timedelta(hours=1)
        title, entry = self.create_entry_with_title(published=True, 
            published_at=published_at)
        response = self.client.get(reverse('en:blog_rss_tagged', kwargs={'tag': 'test'}))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'in English')  
        
    def test_06_posts_tagged_all_languages(self):
        published_at = datetime.datetime.now() - datetime.timedelta(hours=1)
        title, entry = self.create_entry_with_title(published=True, 
            published_at=published_at)
        response = self.client.get(reverse('en:blog_rss_any_tagged', kwargs={'tag': 'test'}))
        self.assertEquals(response.status_code, 200)
        self.assertNotContains(response, 'in English') 
    
    def test_07_no_multilingual(self):
        mwc = [mw for mw in settings.MIDDLEWARE_CLASSES if mw != 'cmsplugin_blog.middleware.MultilingualBlogEntriesMiddleware']
        with SettingsOverride(MIDDLEWARE_CLASSES=mwc):
            published_at = datetime.datetime.now() - datetime.timedelta(hours=1)
            title, entry = self.create_entry_with_title(published=True, 
                published_at=published_at)
            response = self.client.get(reverse('en:blog_rss'))
            self.assertEquals(response.status_code, 200)
            self.assertNotContains(response, 'in English')
            
                
class ViewsTestCase(BaseBlogTestCase):
    
    def test_01_generics(self):
        user = User.objects.all()[0]
        
        published_at = datetime.datetime.now() - datetime.timedelta(hours=1)
        title, entry = self.create_entry_with_title(published=True, 
            published_at=published_at, author=user)
        entry.tags = 'test'
        entry.save()
        
        response = self.client.get(reverse('en:blog_archive_index'))
        self.assertEquals(response.status_code, 200)
        
        response = self.client.get(reverse('en:blog_archive_year', kwargs={'year': published_at.strftime('%Y')}))
        self.assertEquals(response.status_code, 200)
        
        response = self.client.get(reverse('en:blog_archive_month',
            kwargs={
                'year': published_at.strftime('%Y'),
                'month': published_at.strftime('%m')
            }))
        self.assertEquals(response.status_code, 200)
        
        response = self.client.get(reverse('en:blog_archive_day',
            kwargs={
                'year': published_at.strftime('%Y'),
                'month': published_at.strftime('%m'),
                'day': published_at.strftime('%d')
            }))
        self.assertEquals(response.status_code, 200)
        
        response = self.client.get(reverse('en:blog_detail',
            kwargs={
                'year': published_at.strftime('%Y'),
                'month': published_at.strftime('%m'),
                'day': published_at.strftime('%d'),
                'slug': title.slug
            }))
        self.assertEquals(response.status_code, 200)
        
        response = self.client.get(reverse('en:blog_archive_tagged',
            kwargs={
                'tag': 'test'
            }))
        self.assertEquals(response.status_code, 200)
        
        response = self.client.get(reverse('en:blog_archive_author',
            kwargs={
                'author': user.username
            }))
        self.assertEquals(response.status_code, 200)
        
        self.client.login(username='admin', password='admin')

        response = self.client.get(reverse('en:blog_detail',
            kwargs={
                'year': published_at.strftime('%Y'),
                'month': published_at.strftime('%m'),
                'day': published_at.strftime('%d'),
                'slug': title.slug
            }))
        self.assertEquals(response.status_code, 200)
        
class LanguageChangerTestCase(BaseBlogTestCase):
    
    def test_01_language_changer(self):
        published_at = datetime.datetime(2011, 8, 31, 11, 0)
        title, entry = self.create_entry_with_title(published=True, 
            published_at=published_at)
        de_title = self.create_entry_title(entry, title='german', language='de')
        
        from django.utils.translation import activate
        activate('en')
        self.assertEquals(entry.get_absolute_url(), u'/test-page-1/2011/08/31/entry-title/')

        self.assertEquals(entry.get_absolute_url('en'), u'/test-page-1/2011/08/31/entry-title/')
        self.assertEquals(entry.language_changer('en'), u'/test-page-1/2011/08/31/entry-title/')
        self.assertEquals(entry.language_changer('de'), u'/test-page-1/2011/08/31/german/')
        self.assertEquals(entry.language_changer('nb'), u'/test-page-1/')
        self.assertEquals(entry.language_changer('nn'), u'/')
        
class RedirectTestCase(BaseBlogTestCase):
    
    def test_01_redirect_existing_language(self):
        published_at = datetime.datetime(2011, 8, 31, 11, 0)
        title, entry = self.create_entry_with_title(published=True, 
            published_at=published_at, language='de')
            
        with SettingsOverride(DEBUG=True):
            self.client.get(u'/en/')
            mwc = [mw for mw in settings.MIDDLEWARE_CLASSES if mw != 'cmsplugin_blog.middleware.MultilingualBlogEntriesMiddleware']
            with SettingsOverride(MIDDLEWARE_CLASSES=mwc):
                response = self.client.get(u'/test-page-1/2011/08/31/entry-title/')
	        self.assertEqual(response.status_code, 404)
	        
            response = self.client.get(u'/test-page-1/2011/08/31/entry-title/')
            self.assertRedirects(response, u'/de/test-page-1/2011/08/31/entry-title/')
            
            response = self.client.get(u'/de/test-page-1/2011/08/31/entry-title/')
            self.assertEqual(response.status_code, 200)

            self.create_entry_title(entry, language='nb')
            self.client.get(u'/en/')
            response = self.client.get(u'/test-page-1/2011/08/31/entry-title/')
            self.assertEqual(response.status_code, 404)
            entry.delete()
            response = self.client.get(u'/de/')
            response = self.client.get(u'/test-page-1/2011/08/31/entry-title/')
            self.assertEqual(response.status_code, 404)
         
class LatestEntriesTestCase(BaseBlogTestCase):
    
    def test_01_plugin(self):
        class MockRequest(object):
            LANGUAGE_CODE = 'en'
            REQUEST = {}
        r = MockRequest()
        published_at = datetime.datetime(2011, 8, 30, 11, 0)
        title, entry = self.create_entry_with_title(published=True, 
            published_at=published_at, language='en', title='english title')
        title, entry = self.create_entry_with_title(published=True, 
            published_at=published_at, language='de', title='german title')
        ph = Placeholder(slot='main')
        ph.save()
        from django.utils.translation import activate
        activate('en')
        plugin = LatestEntriesPlugin(placeholder=ph, plugin_type='CMSLatestEntriesPlugin', limit=2, current_language_only=True)
        plugin.insert_at(None, position='last-child', save=False)
        plugin.save()
        self.assertEquals(plugin.render_plugin({'request': r}).count('english title'), 1)
        self.assertEquals(plugin.render_plugin({'request': r}).count('german title'), 0)
        plugin = LatestEntriesPlugin(placeholder=ph, plugin_type='CMSLatestEntriesPlugin', limit=2, current_language_only=False)
        plugin.insert_at(None, position='last-child', save=False)
        plugin.save()
        self.assertEquals(plugin.render_plugin({'request': r}).count('english title'), 1)
        self.assertEquals(plugin.render_plugin({'request': r}).count('german title'), 1)

        
class SitemapsTestCase(BaseBlogTestCase):
    
    def test_01_sitemaps(self):
        published_at = datetime.datetime.now() - datetime.timedelta(hours=1)
        title, entry = self.create_entry_with_title(published=True, 
            published_at=published_at)
        response = self.client.get('/sitemap.xml')
        self.assertEquals(response.status_code, 200)
