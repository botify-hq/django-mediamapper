from setuptools import setup, find_packages

setup(
    name = "Media Mapper",
    version = "0.1",
    packages = find_packages(),
    include_package_data = True,

    author = "Thomas Grange",
    author_email = "thomas@sem.io",
    description = "Plug photos and videos from facebook, youtube, vimeo, dailymotion and many others..",
    license = "Apache",
    keywords = "python django facebook youtube dailymoion vimeo photos videos",
    url = "http://github.com/sem-io/django-mediamapper",
    #dependency_links = ['git://github.com/sem-io/facebook-sdk-fork/#egg=facebook_sdk', 'git://github.com/sem-io/django-extended-choices#egg=extended_choices', 'git://github.com/dkm/python-vimeo.git#egg=vimeo'],
    dependency_links = ['git://github.com/sem-io/facebook-sdk-fork/#egg=facebook_sdk', 'git://github.com/dkm/python-vimeo.git#egg=vimeo', 'git://github.com/sem-io/django-extended-choices.git#egg=extended_choices'],
    install_requires = ['BeautifulSoup>=3.2.0', 'oauth2', 'elementtree', 'facebook_sdk', 'vimeo', 'extended_choices'],

    classifiers = [
        'Development Status :: 0.1 - Early Alpha',
        'Environment :: Unix-like Systems',
        'Intended Audience :: Developers, Project managers, Sys admins',
        'Programming Language :: Python',
        'Operating System :: Unix-like',
    ],
)
