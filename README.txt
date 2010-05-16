ALPHA

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
- django tagging - http://code.google.com/p/django-tagging/
- simple-translation - http://bitbucket.org/fivethreeo/simple-translation/

Setup
- make sure requirements are installed and properly working
- add cmsplugin_blog to python path
- add 'cmsplugin_blog' to INSTALLED_APPS
- (optional) add 'simple_translation.middleware.MultilingualGenericsMiddleware' to MIDDLEWARE_CLASSES
- run 'python manage.py syncdb'
- Create a page in cms and in the 'advanced settings' section of the admin for that page for 'application' select 'Blog' (Restart of the server required due to caching!)
