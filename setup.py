from setuptools import setup

setup(
    name = "Media Mapper",
    version = "0.1",
    include_package_data = True,

    author = "Thomas Grange",
    author_email = "thomas@sem.io",
    description = "Plug photos and videos from facebook, youtube, vimeo, dailymotion and many others..",
    license = "Apache",
    keywords = "python django facebook youtube dailymoion vimeo photos videos",
    url = "http://github.com/sem-io/django-mediamapper",
    install_requires = ['BeautifulSoup>=3.2.0', 'oauth2', 'elementtree'],

    classifiers = [
        'Development Status :: 0.1 - Early Alpha',
        'Environment :: Unix-like Systems',
        'Intended Audience :: Developers, Project managers, Sys admins',
        'Programming Language :: Python',
        'Operating System :: Unix-like',
    ],
)
