from setuptools import setup, find_packages
setup(
    name='cmsplugin-blog',
    version='0.9.2',
    description='This is a blog app/plugin for django-cms 2.0',
    author='Oyvind Saltvik',
    author_email='oyvind@gmail.com',
    url='http://github.com/fivethreeo/cmsplugin-blog/',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    test_suite = "cmsplugin_blog.testing.run_tests.run_tests",
    include_package_data=True,
    zip_safe=False,
    install_requires=['simple-translation', 'djangocms-utils', 'django-tagging', 'django-cms==2.1.0.rc2', 'sphinx'],
)
