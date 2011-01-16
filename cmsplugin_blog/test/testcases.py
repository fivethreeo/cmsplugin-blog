from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from cms.test.testcases import CMSTestCase
from cms.models.titlemodels import Title

from cmsplugin_blog.models import Entry, EntryTitle

class BaseBlogTestCase(CMSTestCase):

    def setUp(self):
        superuser = User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
        page = self.create_page(user=superuser, published=True)
        english_title = page.title_set.all()[0]
        self.assertEquals(english_title.language, 'en')
        Title.objects.create(
            language='de',
            title='%s DE' % english_title.title,
            slug=english_title.slug,
            path=english_title.path,
            page=page
        )
        page.title_set.all().update(application_urls='BlogApphook')
        
    def create_entry_with_title(self, title=None, slug=None, language=None, published=False, published_at=None, author=None):
        kwargs = {'is_published': published}
        if published_at:
            kwargs['pub_date'] = published_at
        entry = Entry.objects.create(**kwargs)
        entrytitle = self.create_entry_title(entry, title=title, slug=slug, language=language, author=author)
        return (entrytitle, entry)
        
    def create_entry_title(self, entry, title=None, slug=None, language=None, author=None):
        if not title:
            title = 'Entry title'
        slug = slug or slugify(title)
        language = language or 'en'
        return entry.entrytitle_set.create(entry=entry, title=title, slug=slug, language=language, author=author)