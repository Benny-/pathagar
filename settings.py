
"""
This settings are for testing Pathagar with the Django development
server.  It will use a SQLite database in the current directory and
Pathagar will be available at http://127.0.0.1:8000 loopback address.

For production, you should use a proper web server to deploy Django,
serve static files, and setup a proper database.

"""


import os


# Books settings:

BOOKS_PER_PAGE = 80 # Number of books shown per page in the OPDS
                    # for the catalogs feeds and in the HTML pages.
AUTHORS_PER_PAGE = 750

SEARCH_SHORTNAME = u"My Little Pony"
SEARCH_DESCRIPTION = u"Ebooks from fimfiction.net"

FEED_TITLE = u'My Little Pony'
FEED_ICON_LOCATION = u'/static/images/elements_of_harmony_dictionary_icon_by_xtux345-d4myvo7.png'
FEED_DESCRIPTION = u'Ebooks from fimfiction.net'

# A link to the ebook transformer service. https://github.com/Benny-/fim-ebook-transformer
# Users who wish to download a ebook are redirected to this service.
FIM_EBOOK_TRANSFORMER = u'http://fimfiction.djazz.se/story/{}/download/fimfic_{}.epub'

BOOKS_STATICS_VIA_DJANGO = True

# sendfile settings:

SENDFILE_BACKEND = 'sendfile.backends.development'

# Get current directory to get media and templates while developing:
CUR_DIR = u'' + os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(CUR_DIR, 'database.db'),
    }
}

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

MEDIA_ROOT = os.path.join(CUR_DIR, 'static_media')

MEDIA_URL = '/static_media/'

SECRET_KEY = '7ks@b7+gi^c4adff)6ka228#rd4f62v*g_dtmo*@i62k)qn=cs'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'pathagar.urls'

INTERNAL_IPS = ('127.0.0.1',)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)

STATIC_ROOT = os.path.join(CUR_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(CUR_DIR, 'static'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'tagging', # TODO old
    'taggit',
    'pathagar.books',
)

