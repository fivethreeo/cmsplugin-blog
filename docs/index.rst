.. simple-translation documentation master file, created by
   sphinx-quickstart on Tue Aug 31 16:36:25 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=====================
cmsplugin-blog
=====================

.. module:: cmsplugin-blog
   :synopsis: cmsplugin-blog

Features
========
* multilanguage posts
* editing of content using django cms plugins
* plugin for django cms for showing latest entries
* feeds for languages / tags

Overview
========

There are six steps for using cmsplugin-blog:

    1. Install ``cmsplugin-blog`` and dependencies.
    
        Install django-cms as per install docs on http://django-cms.rtfd.org/.
        
        Install ``cmsplugin-blog`` from pypi: ::
        
            pip install cmsplugin-blog # also installs dependencies
        
    2. Add ``cmsplugin_blog``, ``djangocms_utils``, ``tagging`` and ``simple_translation`` to ``settings.INSTALLED_APPS``
    
        Optionally set the placeholders in settings.py. ::
            
            CMSPLUGIN_BLOG_PLACEHOLDERS = ('first', 'second', 'third')
        
    3. Sync the database. ::
        
            python manage.py syncdb
            
            # or if south is installed
            python manage.py syncdb --all
            python manage.py migrate --fake    
        
    4. If you are interested in multilangual blog, add ``cmsplugin_blog.middleware.MultilingualBlogEntriesMiddleware`` to ``settings.MIDDLEWARE_CLASSES``
    
    5. Put a template adapted to your site in ``templates/cmsplugin_blog/cmsplugin_blog_base.html``.
    
        Blocks in default templates are 'left-col' and 'right-col'.
        
    6. Create a page in the cms and in 'Application' in the 'Advanced settings' section
        of the admin select 'Blog Apphook'
        
        Do this for each language you want to show posts in.
        (Restart of the server required due to caching!)
    
    
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

