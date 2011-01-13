
def runtests():
    
    from django.test.utils import get_runner
    from django.conf import settings
    
    settings.configure(
        INSTALLED_APPS=[
            'cmsplugin_blog.testing.testapp',
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
        )
    )
    
    test_runner = get_runner(settings)
    failures = test_runner([])
    sys.exit(failures)

if __name__ == '__main__':
    runtests()