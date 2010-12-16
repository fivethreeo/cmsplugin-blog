BETA

Name: cmsplugin-blog
Description: A blog plugin for django-cms
Download: http://bitbucket.org/fivethreeo/cmsplugin-blog/

Features:
- multilanguage posts
- editing of content using django cms plugins
- plugin for django cms for showing latest entries
- feeds for languages / tags

Requires:
- django-cms 2.1

Setup
- make sure requirements are installed and properly working
    pip install -e git+https://github.com/divio/django-cms.git#egg=django-cms # until a stable hits pypi
    pip install cmsplugin_blog # should do it
- follow install for django-cms http://django-cms.readthedocs.org/ 
- add 'cmsplugin_blog' to INSTALLED_APPS
- for multilanguage posts :
    add 'cms.middleware.multilingual.MultilingualURLMiddleware'
    add 'simple_translation.middleware.MultilingualGenericsMiddleware' 
    to MIDDLEWARE_CLASSES 
- run 'python manage.py syncdb'
- create a page in cms and in the 'Advanced settings' section of the admin for that page for 'Application' select 'Blog Apphook'
  Do this for each language you want to show posts in.
  (Restart of the server required due to caching!)
