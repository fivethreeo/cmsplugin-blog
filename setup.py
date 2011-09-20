from setuptools import setup, find_packages
import os

import cmsplugin_blog

CLASSIFIERS = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
]

setup(
    name='cmsplugin-blog',
    version=cmsplugin_blog.get_version(),
    description='This is a blog app/plugin for django-cms 2.2',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.txt')).read(),
    author='Oyvind Saltvik',
    author_email='oyvind.saltvik@gmail.com',
    url='http://github.com/fivethreeo/cmsplugin-blog/',
    packages=find_packages(),
    package_data={
        'cmsplugin_blog': [
            'static/cmsplugin_blog/*',
            'locale/*/LC_MESSAGES/*',
        ]
    },
    classifiers=CLASSIFIERS,
    test_suite = "cmsplugin_blog.test.run_tests.run_tests",
    include_package_data=True,
    zip_safe=False,
    install_requires=['django-cms', 'simple-translation', 'djangocms-utils', 'django-tagging'],
)
