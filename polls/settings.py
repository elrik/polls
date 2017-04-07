"""
Django settings for polls project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.join(BASE_DIR, "polls")

sys.path.insert(1, os.path.join(PROJECT_ROOT, 'apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z&dlztdid#a0#y4etp4blo!1s=5r+w^ng=+^cmpzn@9+@8ha5p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Standard apps
    'debug_toolbar',
    'django_extensions',
    'pipeline',
    'channels',
    'docs',


    # Project apps
    'core',
    'questionpoll.apps.QuestionPollConfig',
]

# Should be changed to MIDDLEWARE but because of DjDT and patch settings
# we are using old name
MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
]

ROOT_URLCONF = 'polls.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_ROOT, "templates"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.development_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'polls.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'pipeline.finders.CachedFileFinder',
    'pipeline.finders.PipelineFinder',
)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(
    PROJECT_ROOT,
    "site_media",
    "static",
)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(
    PROJECT_ROOT,
    "site_media",
    "media",
)

# Set development email port
EMAIL_PORT = 1025

# Should debug toolbar patch settings
DEBUG_TOOLBAR_PATCH_SETTINGS = DEBUG

# Should we compile less files clientside
LESS_COMPILE_CLIENTSIDE = DEBUG

PIPELINE = {
    'PIPELINE_ENABLED': DEBUG is False,
    'PIPELINE_COLLECTOR_ENABLED': True,
    'JAVASCRIPT': {
        'vendor': {
            'source_filenames': (
                'core/vendor/jquery-3.1.0.min.js',
                'core/vendor/bootstrap-3.3.7/js/bootstrap.min.js',
                'core/vendor/d3/d3.min.js',
                'core/vendor/c3/c3.min.js',
            ),
            'output_filename': 'js/vendor.js',
        },
        'app': {
            'source_filenames': (
                'channels/js/websocketbridge.js',
                'core/js/main.js',
            ),
            'output_filename': 'js/app.js',
        },
    },
    'STYLESHEETS': {
        'vendor': {
            'source_filenames': (
                'core/vendor/bootstrap-3.3.7/css/bootstrap.min.css',
                'core/vendor/font-awesome-4.6.3/css/font-awesome.min.css',
                'core/vendor/c3/c3.min.css',
            ),
            'output_filename': "css/vendor.css",
        },
        'app': {
            'source_filenames': (
                'core/less/main.less',
            ),
            'output_filename': "css/app.css",
        },
    },
    'COMPILERS': (
        'pipeline.compilers.less.LessCompiler',
    ),
    'CSS_COMPRESSOR': 'pipeline.compressors.yuglify.YuglifyCompressor',
    'JS_COMPRESSOR': 'pipeline.compressors.yuglify.YuglifyCompressor',
}


# In settings.py
CHANNEL_LAYERS = {
    "default": {
        # "BACKEND": "asgiref.inmemory.ChannelLayer",
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "ROUTING": "polls.routing.channel_routing",
    },
}

DOCS_ROOT = os.path.join(BASE_DIR, 'docs/_build/html')
DOCS_ACCESS = 'staff'

# If we have external settings load data
if os.path.exists(
        os.path.abspath(os.path.join(BASE_DIR, 'config/settings.py'))):
    with open(os.path.abspath(
            os.path.join(BASE_DIR, 'config/settings.py'))) as f:
        exec f
