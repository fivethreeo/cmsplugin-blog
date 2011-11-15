.. toctree::

##############
cmsplugin-blog
##############

cmsplugin-blog is really simple to set up on a working installation of django CMS.

************
Requirements
************

* `django CMS`_ 2.2
* `djangocms-utils`_ 0.9.5+
* `simple-translation`_ 0.8.5+
* `jQuery`_ 1.4.4+
* `jQuery UI`_ 1.8.1+
* `django-tagging`_ 0.3+
* `django-missing`_
* `django-guardian`_ (optional)

On Django 1.2.7:
* `django-cbv`_

.. note :: jQuery can be provided either by locally or linking to a public server, like Google's or Microsoft's CDN.

.. _django CMS: https://www.django-cms.org/
.. _django-staticfiles: http://pypi.python.org/pypi/django-staticfiles/
.. _django-tagging: http://code.google.com/p/django-tagging/
.. _djangocms-utils: https://github.com/fivethreeo/djangocms-utils
.. _simple-translation: https://github.com/fivethreeo/simple-translation
.. _jQuery: http://jquery.com/
.. _jQuery UI: http://jqueryui.com/
.. _django-cbv: http://pypi.python.org/pypi/django-cbv
.. _django-missing: https://bitbucket.org/mitar/django-missing
.. _django-guardian: http://readthedocs.org/docs/django-guardian/en/v1.0.2/

Installation
============

Install ``cmsplugin-blog`` from pypi: ::

    pip install cmsplugin-blog

.. note :: When installing the cmsplugin-blog using pip `django-tagging`_, `django-missing`_, `djangocms-utils`_, and `simple-translation`_ will be installed automatically.

***********************
Configuration and setup
***********************

Settings
========
Add the following apps to your :setting:`django:INSTALLED_APPS` which enable cmsplugin-blog
and required or highly recommended applications/libraries):

* ``'cmsplugin_blog'``, cmsplugin-blog itself
* ``'djangocms_utils'``, utilities and extensions to django CMS
* ``'simple_translation'``, enables multilingual features
* ``'tagging'``, enables tagging of posts
* ``'staticfiles'``, for serving static files ::
* ``'missing'``, provides improved slug generation
* ``'guardian'``, provides per-object-permissions (see docs for `django-guardian`_)

Add required settings::

    INSTALLED_APPS = (
        ...
        'cmsplugin_blog',
        'djangocms_utils',
        'simple_translation',
        'tagging',
        'staticfiles',
        'missing',
        'guardian', # optional
        ...
    )

For Django < 1.3 you need django-cbv for support for class-based views and you should also add ``cbv.middleware.DeferredRenderingMiddleware`` to :setting:`django:MIDDLEWARE_CLASSES` ::

    MIDDLEWARE_CLASSES = (
        ...
        'cbv.middleware.DeferredRenderingMiddleware',
    )

Static content
--------------
Set the ``STATIC_ROOT`` and ``STATIC_URL`` settings for ``django-staticfiles``.::

    STATIC_ROOT = '/projectpath/static/'
    STATIC_URL = '/static/'


jQuery and jQuery UI
--------------------

Add the following settings to add jQuery UI ::

    JQUERY_JS = 'https://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js'
    JQUERY_UI_JS = 'https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.12/jquery-ui.min.js'
    JQUERY_UI_CSS = 'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.12/themes/smoothness/jquery-ui.css'

Or download the sources and make them available locally::

    JQUERY_UI = '/path/to/jquery/'
    JQUERY_JS = '%sjs/jquery-1.4.4.min.js' % JQUERY_UI
    JQUERY_UI_JS = '%sjs/jquery-ui-1.8.9.custom.min.js' % JQUERY_UI
    JQUERY_UI_CSS = '%scss/smoothness/jquery-ui-1.8.9.custom.css' % JQUERY_UI

Multilingual blog
-----------------
If you are interested in multilingual blog, add ``cmsplugin_blog.middleware.MultilingualBlogEntriesMiddleware`` to :setting:`django:MIDDLEWARE_CLASSES` ::

    MIDDLEWARE_CLASSES = (
        ...
        'cmsplugin_blog.middleware.MultilingualBlogEntriesMiddleware',
    )

Blog entry placeholders
-----------------------
You can create multiple placeholders for each blog entry. This is useful for creating extra fields like excerpt, images, etc.::

    CMSPLUGIN_BLOG_PLACEHOLDERS = ('first', 'second', 'third')

Update the database
===================
Next, you need to update the database with the fields required by cmsplugin-blog::

    python manage.py syncdb

    # or if south is installed
    python manage.py syncdb --all
    python manage.py migrate --fake

*********
Templates
*********
In your ``template`` folder create a template adapted to your site as ``cmsplugin_blog/cmsplugin_blog_base.html``.

For example, if you have a template called ``base.html`` which has a block called ``body`` create a template that looks like this::

    {% extends "base.html" %}

    {% block body %}
        {% block left-col %}{% endblock %}
        {% block right-col %}{% endblock %}
    {% endblock %}

.. note:: The cmsplugin-blog uses the block names ``left-col`` and ``right-col`` by default.

********
Sitemaps
********
If you use the sitemaps framework in your cms, you can add your blog entry pages to the sitemaps.xml file by including the sitemap class in your urls.py.

e.g. ::

    from cms.sitemaps import CMSSitemap
    from cmsplugin_blog.sitemaps import BlogSitemap

    urlpatterns = patterns('',
        url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {
            'sitemaps': {
                'cmspages': CMSSitemap,
                'blogentries': BlogSitemap
            }
        }),  
        url(r'^', include('cms.urls'))
    )

*****************
Creating the blog
*****************
To create a blog you need to create a page which will contain the root of the blog. From this page the entire
blog is shown.

Create a page in the CMS. Under ``Advanced settings`` ``Application``, select ``Blog Apphook``.

Do this for each language you want to show posts in. A restart of the server afterwards is mandatory due to caching.

That should be it! Now you can spend countless hours and nights thinking about what you were supposed to write about
that wasn't kittens or other cute furry animals.

