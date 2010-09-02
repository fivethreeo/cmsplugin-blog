BETA

Name: cmsplugin-blog
Description: A blog plugin for django-cms
Download: http://bitbucket.org/fivethreeo/cmsplugin-blog/

Features:
- multilanguage posts
- editing of content using django cms plugins
- plugin for django cms for showing latest entries
- feeds for languages / tags

Requirements:
- django-cms-2.0
- django-tagging - http://code.google.com/p/django-tagging/
- django-multilingual-ng - http://github.com/ojii/django-multilingual-ng/
- simple-translation - http://bitbucket.org/fivethreeo/simple-translation/

Setup
- make sure requirements are installed and properly working
- add cmsplugin_blog to python path
- add 'cmsplugin_blog' to INSTALLED_APPS
- add 'multilingual.context_processors.multilingual' to TEMPLATE_CONTEXT_PROCESSORS
- for multilanguage posts :
    add 'simple_translation.middleware.MultilingualGenericsMiddleware' 
    and 'cms.middleware.multilingual.MultilingualURLMiddleware'
    to MIDDLEWARE_CLASSES 
- if you *DONT* want multilanguage posts you need to add 'django.middleware.locale.LocaleMiddleWare' to MIDDLEWARE_CLASSES
- run 'python manage.py syncdb'
- Create a page in cms and in the 'Advanced settings' section of the admin for that page for 'Application' select 'Blog Apphook'
  Do this for each language you want to show posts in.
  (Restart of the server required due to caching!)
