import sys
import os
import django

INSTALLED_APPS = [
    'cmsplugin_blog.test.testapp',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',        
    'cms',
    'cms.plugins.text',
    'mptt',
    'menus',
    'tagging',
    'simple_translation',    
    'cmsplugin_blog',
    'djangocms_utils',
    'sekizai'
]

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.csrf.middleware.CsrfViewMiddleware',
    'cms.middleware.multilingual.MultilingualURLMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cmsplugin_blog.middleware.MultilingualBlogEntriesMiddleware'
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.core.context_processors.auth",
    "django.core.context_processors.i18n",
    "django.core.context_processors.debug",
    "django.core.context_processors.request",
    "django.core.context_processors.media"
]

if django.VERSION[1] < 3: # pragma: no cover
    MIDDLEWARE_CLASSES.insert(12, 'cbv.middleware.DeferredRenderingMiddleware')
    INSTALLED_APPS.append('staticfiles')
    INSTALLED_APPS.append('cbv')
    TEMPLATE_CONTEXT_PROCESSORS.append('staticfiles.context_processors.static')
else:
    INSTALLED_APPS.append('django.contrib.staticfiles')
    TEMPLATE_CONTEXT_PROCESSORS.append('django.core.context_processors.static')
    
def run_tests():
    
    from django.conf import settings
    
    settings.configure(
        INSTALLED_APPS=INSTALLED_APPS,
        MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES,
        TEMPLATE_CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS,
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'blog_tests.db',
            }
        },
        CMS_TEMPLATES = (
            ('nav_playground.html', 'default'),
        ),
        ROOT_URLCONF='cmsplugin_blog.test.testapp.urls',
        USE_I8N=True,
        LANGUAGE_CODE='en',
        LANGUAGES=(('en', 'English'),('de','German'),('nb','Norwegian'),('nn','Norwegian Nynorsk')),
        JQUERY_UI_CSS='',
        JQUERY_JS='',
        JQUERY_UI_JS='',
        STATIC_URL='/some/url/',
        STATIC_ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, os.path.pardir),
        TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner',
        TEST_OUTPUT_VERBOSE = True
    )
    
    from django.test.utils import get_runner

    failures = get_runner(settings)().run_tests(['cmsplugin_blog'])
    sys.exit(failures)

if __name__ == '__main__':
    run_tests()
