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
    install_requires = ['BeautifulSoup>=3.2.0', 'oauth2', 'elementtree'],
    dependency_links = ['http://github.com/sem-io/facebook-sdk-fork#facebook_sdk#egg=facebook', 'http://github.com/twidi/django-extended-choices.git#egg=extended_choices', 'git://github.com/dkm/python-vimeo.git#egg=vimeo'],

    classifiers = [
        'Development Status :: 0.1 - Early Alpha',
        'Environment :: Unix-like Systems',
        'Intended Audience :: Developers, Project managers, Sys admins',
        'Programming Language :: Python',
        'Operating System :: Unix-like',
    ],
)
