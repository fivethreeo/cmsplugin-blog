from setuptools import setup, find_packages
setup(
    name='cmsplugin-blog',
    version='0.9b',
    description='This is a blog app/plugin for django-cms 2.0',
    author='Oyvind Saltvik',
    author_email='oyvind@gmail.com',
    url='http://bitbucket.org/fivethreeo/cmsplugin-blog/',
    packages=find_packages(),
    package_data={'': ['templates/*/*.html']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools'],
)
