ALPHA

Name: cmsplugin-blog
Description: A blog plugin for django-cms
Download: http://bitbucket.org/fivethreeo/cmsplugin-blog/

Requirements:
- django-cms-2.0
- simple-translation - http://bitbucket.org/fivethreeo/simple-translation

Setup
- make sure requirements are installed and properly working
- add cmsplugin_blog to python path
- add 'cmsplugin_blog' to INSTALLED_APPS
- run 'python manage.py syncdb'
- Create a page in cms and in the 'advanced settings' section of the admin for that page for 'application' select 'Blog' (Restart of the server required due to caching!)
