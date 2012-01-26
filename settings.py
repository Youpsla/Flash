# -*- coding: utf-8 -*-

# Django settings for flash project.
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS



DEBUG = True

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Alain - Admin Django', 'youpsla@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'flash',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'FR-fr'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = 'C:/dev/html/flash/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = ( 'C:/dev/Instantaneus/Instantaneus/html/static',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'bhiz$kd$n=#5)ez*8=_whg*ybypykyhe^_*$u*b5#wf!3=d!&x'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    #'django_requestlogging.middleware.LogSetupMiddleware',
)

INTERNAL_IPS = ('127.0.0.1','localhost')

ROOT_URLCONF = 'Instantaneus.urls'

TEMPLATE_DIRS = ( 'C:/dev/Instantaneus/Instantaneus/html',
)

TEMPLATE_CONTEXT_PROCESSORS += (
     'django.core.context_processors.request',
     
) 


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.free.fr'

EMAIL_PORT = '587'

DEFAULT_FROM_EMAIL= 'youpsla@free.fr'

EMAIL_HOST_USER = 'youpsla@free.fr'

EMAIL_HOST_PASSWORD = '372010'

ACCOUNT_ACTIVATION_DAYS = 7

LOGIN_REDIRECT_URL = '/owner_profil/'

AUTH_PROFILE_MODULE = 'magasins.MagasinOwnerProfile'

SESSION_COOKIE_AGE = 2500

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    # 'SHOW_TOOLBAR_CALLBACK': None,
    # 'SHOW_TEMPLATE_CONTEXT': True,
    # 'EXTRA_SIGNALS': ['myproject.signals.MySignal'],
    # 'HIDE_DJANGO_SQL': False,
    # 'TAG': 'div',
}



INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'django.contrib.admin',
    'categories',
    'magasins',
    'registration',
    'profiles',
    'evenements',
    'clients',
    'commandes',
    'django_mailer',
    #'djangotasks',
    'debug_toolbar',
    'rosetta',
    'bootstrap',
    #'django_requestlogging',

)

#DJANGOTASK_DAEMON_THREAD = True

# DEBUG_TOOLBAR_PANELS = (
    # 'debug_toolbar.panels.version.VersionDebugPanel',
    # 'debug_toolbar.panels.timer.TimerDebugPanel',
    # 'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    # 'debug_toolbar.panels.headers.HeaderDebugPanel',
    # 'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    # 'debug_toolbar.panels.template.TemplateDebugPanel',
    # 'debug_toolbar.panels.sql.SQLDebugPanel',
    # 'debug_toolbar.panels.signals.SignalDebugPanel',
    # 'debug_toolbar.panels.logger.LoggingPanel',
# )
# 


ANONYMOUS_USER_ID = -1

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
#    'handlers': {
#        'mail_admins': {
#            'level': 'ERROR',
#            'class': 'django.utils.log.AdminEmailHandler'
#        }
#    },
#    'loggers': {
#        'django.request': {
#            'handlers': ['mail_admins'],
#            'level': 'ERROR',
#            'propagate': True,
#        },
#    }
#}
import os

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
#    'filters': {
#                'request':{
#                           '()': 'django_requestlogging.logging_filters.RequestFilter',
#                           }
#                },
    'formatters': {
            'verbose': {
                    #'format': '%(levelname)-8s %(remote_addr)-15s %(path_info)s %(asctime)s %(name)-20s %(funcName)-15s %(message)s'
                    'format': '%(levelname)-8s %(asctime)s %(name)-20s %(funcName)-15s %(message)s'
                    },
            'simple': {
                       'format': '%(levelname)s %(message)s'
                       },
            },
    'handlers': {
            'normal': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            #'filters': ['request'],
            'formatter': 'verbose',
            'filename': os.path.join('C:/dev/Instantaneus/Instantaneus/html/static', 'log', 'normal.log')
            },
            'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            #'filters': ['request'],
            'formatter': 'verbose',
            },
        },
    'loggers': {
        'Instantaneus': {
                    'handlers': ['normal','console'],
                    'level': 'DEBUG',
                    #'filters': ['request'],
                    'propagate': True,
                    },
        'evenements': {
                    'handlers': ['normal','console'],
                    'level': 'DEBUG',
                    #'filters': ['request'],
                    'propagate': True,
                    },
                }
           }

