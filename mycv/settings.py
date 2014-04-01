"""
Django settings for MyCV project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6.1/ref/settings/
"""
import os

from configurations import Configuration, values


class Common(Configuration):

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    SECRET_KEY = ';alksdfjpozixuf2ew/.,mz'

    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

    ALLOWED_HOSTS = []

    ADMINS = (('Philip Kalinsky', 'pkalinsky@greenlightgo.co'), )

    DATE_FORMAT = '%m/%d/%Y'

    EMAIL = values.EmailURLValue('console://')
    DEFAULT_FROM_EMAIL = 'noreply@slipperyslo.pe'
    NOREPLY_EMAIL = 'noreply@slipperyslo.pe'

    INTERNAL_IPS = ('127.0.0.1',)

    MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

    SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

    # Application definition

    INSTALLED_APPS = (
        'grappelli.dashboard',
        'grappelli',

        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.humanize',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'mycv.apps.core',
        'mycv.apps.projects',

        # Need this after web.admin because of test runner:
        # it loads django admin tests by 'admin' app label first
        'django.contrib.admin',

        # 3rd party
        'django_extensions',
        'south',
        #south installs its own test command that turns off migrations during testing.
        #Make sure that django-nose comes after south
        #'django_nose',
    )

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.gzip.GZipMiddleware',
        'django.middleware.transaction.TransactionMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        #'django.middleware.cache.UpdateCacheMiddleware',
        'django.middleware.common.CommonMiddleware',
        #'django.middleware.cache.FetchFromCacheMiddleware',
    )

    ROOT_URLCONF = 'mycv.urls'

    WSGI_APPLICATION = 'mycv.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#databases
    # http://django-configurations.readthedocs.org/en/latest/values/#configurations.values.DatabaseURLValue
    DATABASES = values.DatabaseURLValue(
        'sqlite:///%s' % os.path.join(BASE_DIR, 'db.sqlite3'), environ=True
    )

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    SITE_ID = 1

    # Localization
    LANGUAGE_CODE = 'en'
    LOCALE_PATHS = (
        os.path.join(BASE_DIR, 'mycv', 'locale'),
    )
    ugettext = lambda s: s

    LANGUAGES = (
        ('en', ugettext('English')),
    )

    USE_I18N = False
    USE_L10N = False
    TIME_ZONE = 'America/New_York'
    USE_TZ = True

    GEOIP_DATABASE = os.path.join(
        os.environ.get("GEOLITECITY_DB_DIR", '/var/local/venv/mycv/var/data'), 'GeoLiteCity.dat'
    )

    # Static files (CSS, JavaScript, Images)
    MEDIA_ROOT = os.environ.get("DJANGO_MEDIA_ROOT", os.path.join(BASE_DIR, 'media'))
    MEDIA_URL = '/media/'

    STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected')
    STATIC_URL = '/static/'

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'mycv', 'static'),
    )
    TEMPLATE_DIRS = (
        os.path.join(BASE_DIR, 'mycv', 'templates'),
    )
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )
    #DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.messages.context_processors.messages',
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        #'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.request',
    )
    # i cannot get the templates invalidated from this loader cache!!!
    # do not use for now.

    #TEMPLATE_LOADERS = (
    #    ('django.template.loaders.cached.Loader', (
    #    ('mycv.libs.loaders.cached.Loader', (
    #        'django.template.loaders.filesystem.Loader',
    #        'django.template.loaders.app_directories.Loader',
    #    )),
    #)

    CACHES = values.CacheURLValue('memcached://127.0.0.1:11211/')

    #django-grappelli
    #GRAPPELLI_INDEX_DASHBOARD = 'mycv.libs.grappelli.dashboard.CustomIndexDashboard'
    GRAPPELLI_ADMIN_TITLE = "mycv CMS"

    LOGFILE = os.environ.get("DJANGO_LOG", "/var/local/log/mycv.log")

    #enabling sorl log handler will send emails for each missing thumbnail
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOGFILE,
                'maxBytes': 1024*1024*5, # 5 MB
                'backupCount': 5,
                'formatter': 'standard',
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'include_html': False,
            },
            'request_handler': {
                'class': 'django.utils.log.NullHandler',
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': 'DEBUG',
                'propagate': True
            },
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
            'django.db.backends': { # Stop SQL debug from logging to main logger
                'handlers': ['request_handler'],
                'level': 'DEBUG',
                'propagate': False
            },
        }
    }


class Dev(Common):
    """
    The in-development settings and the default configuration.
    """

    # this setting is useful for debugging but it will break the admin.
    # You have been warned.
    #TEMPLATE_STRING_IF_INVALID = 'undefined variable [%s]'

    SECRET_KEY = '[a09s8=b-axm;lk123'

    DATABASES = values.DatabaseURLValue('postgres://mycv:@localhost:5433/mycv')

    ALLOWED_HOSTS = ['.slipperyslo.pe', ]

    #STATICFILES_STORAGE = (
    #    'django.contrib.staticfiles.storage.StaticFilesStorage'
    #)
    #Common.INSTALLED_APPS += ('debug_toolbar', )
    #Common.MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware', )
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]
    SHELL_PLUS_PRE_IMPORTS = (
        #('module.submodule1', ('class1', 'function2')),
        #('module.submodule2', 'function3'),
        #('module.submodule3', '*'),
        #'module.submodule4'
        ('django.db', 'connection'),
        ('django.db', 'reset_queries'),
    )
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        },
    }


class Prod(Common):
    """
    The in-production settings.
    """
    DEBUG = False
    TEMPLATE_DEBUG = False
    THUMBNAIL_DEBUG = False

    ALLOWED_HOSTS = [
        '.slipperyslo.pe',
    ]

    #FIXME  enable cached storage
    #STATICFILES_STORAGE = (
    #    'django.contrib.staticfiles.storage.StaticFilesStorage'
    #)

    SECRET_KEY = values.SecretValue()

    DATABASES = values.DatabaseURLValue(
        'postgres://%s:%s@%s:%s/%s' %
        (
            os.environ.get("DATABASE_USER", ""),
            os.environ.get("DATABASE_PASSWORD", ""),
            os.environ.get("DATABASE_HOST", "localhost"),
            os.environ.get("DATABASE_PORT", "5432"),
            os.environ.get("DATABASE_NAME", "mycv"),
        )
    )
    #CACHES = {
    #    'default': {
    #        'BACKEND': 'cpi.libs.uwsgiutils.uwsgicache.UWSGICache',
    #        'SERIALIZATION_MODULE': 'msgpack',
    #        'DJANGO_QS_SERIALIZE': False,
    #    },
    #    'django_qs': {
    #        'BACKEND': 'cpi.libs.uwsgiutils.uwsgicache.UWSGICache',
    #        'SERIALIZATION_MODULE': 'msgpack',
    #        'DJANGO_QS_SERIALIZE': True,
    #    }
    #}
    EMAIL = values.EmailURLValue('smtp://localhost:25')
