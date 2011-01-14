import sys

def run_tests():
    
    from django.conf import settings
    
    settings.configure(
        INSTALLED_APPS=[
            'cmsplugin_blog.test.testapp',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.admin',
            'django.contrib.sites',        
            'cms',
            'cms.plugins.text',
            'publisher',
            'mptt',
            'menus',
            'tagging',
            'simple_translation',    
            'cmsplugin_blog',
        ],
        MIDDLEWARE_CLASSES = (
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.middleware.doc.XViewMiddleware',
            'django.contrib.csrf.middleware.CsrfMiddleware',
            'cms.middleware.user.CurrentUserMiddleware',
            'cms.middleware.page.CurrentPageMiddleware',
            'cms.middleware.toolbar.ToolbarMiddleware',
            'cms.middleware.media.PlaceholderMediaMiddleware',
            'cms.middleware.multilingual.MultilingualURLMiddleware',
            'simple_translation.middleware.MultilingualGenericsMiddleware'
        ),
        TEMPLATE_CONTEXT_PROCESSORS = (
            "django.core.context_processors.auth",
            "django.core.context_processors.i18n",
            "django.core.context_processors.debug",
            "django.core.context_processors.request",
            "django.core.context_processors.media",
            "cms.context_processors.media",
        ),
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'blog_tests.db',
            }
        },
        CMS_TEMPLATES = (
            ('default.html', 'default'),
        ),
        ROOT_URLCONF='cmsplugin_blog.test.testapp.urls',
        LANGUAGES=(('en', 'en'),('de','de'))
    )
    
    from django.test.utils import get_runner

    failures = get_runner(settings)().run_tests(['cmsplugin_blog'])
    sys.exit(failures)

if __name__ == '__main__':
    run_tests()