"""
Django settings for metatask project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from os.path import join
from datetime import timedelta
import os
import cloudinary

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-g0ww$rrq4y7jlnygg-hl(fwcna$w&s8as1&2h$7h&5+_gtl$f6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
# DEBUG = True

# ALLOWED_HOSTS = ["*"]
ALLOWED_HOSTS = [
    "metatask.ibgyzs.easypanel.host", 
    "www.metatask.ibgyzs.easypanel.host", 
    "metatask-backend.ibgyzs.easypanel.host", 
    "www.metatask-backend.ibgyzs.easypanel.host",
    "localhost"
    ]


CORS_ALLOWED_ORIGINS = [
    "https://metatask.ibgyzs.easypanel.host",
    "https://metatask-backend.ibgyzs.easypanel.host",
]

# CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = [
    'https://metatask-backend.ibgyzs.easypanel.host',
]


cloudinary.config( 
  cloud_name = "dwe58zkhv", 
  api_key = "715688338274166", 
  api_secret = "gfYwU8TwBTmf70moip6Co0s6MDI",
  secure = True
)



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    #packages
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework_simplejwt',
    'rest_framework',
    'rest_framework.authtoken',
    "corsheaders",
    # "django_mysql",
    
    #apps
    "profiles",
    "packages",
    "investment",
    "payments",
    "base",
    "admins",
    "videocontent",
    "tasks",
    "withdrawals",

    # must be placed last,
    'django_cleanup.apps.CleanupConfig',
    
]

AUTH_USER_MODEL = 'profiles.Profile'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "corsheaders.middleware.CorsMiddleware", 
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django.middleware.common.CommonMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'base.api.middlewares.RequestLoggingMiddleware',
]

ROOT_URLCONF = 'metatask.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'metatask.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'metatask',  # Database name
#         'USER': 'postgres',  # PostgreSQL username
#         'PASSWORD': '3f533a950983af8274ef',  # Database password
#         'HOST': 'metatask_metataskdb',  # PostgreSQL host (localhost or IP address)
#         'PORT': '5432',  # Default PostgreSQL port
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Database engine (default: SQLite)
        'NAME': BASE_DIR / 'db.sqlite3',         # Path to the database file
    }
}

# WhiteNoise settings for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True






# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'  # Make sure to include the leading slash

# The directory where static files will be collected
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Additional directories where Django will look for static files
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # This is where you can store your custom static files
]

# Media files (uploaded files)
MEDIA_URL = '/media/'  # Make sure to include the leading slash
MEDIA_ROOT = BASE_DIR / 'media_files'  # This is where uploaded media files will be stored


# settings.py

# Maximum size (in bytes) for data that can be uploaded
DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100 MB

# Maximum size (in bytes) for file uploads
FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100 MB


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# REST_AUTH = {
#     'USE_JWT': True,
#     'USER_DETAILS_SERIALIZER': 'profiles.api.serializers.CustomUserDetailsSerializer',
# }


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
    # 'DEFAULT_FILTER_BACKENDS': (
    #     'django_filters.rest_framework.DjangoFilterBackend',
    # )
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=20),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=25),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "TOKEN_OBTAIN_SERIALIZER": "profiles.api.serializers.CustomUserDetailsSerializer",
}


LOGGING_DIR = os.path.join(BASE_DIR, "loggers")
STATIC_DIR = os.path.join(BASE_DIR, "static")

if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)
    
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, "project_debug.log"),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'request_file': {
            'level': 'INFO',
            'class': 'base.api.logging_handlers.RequestLoggingHandler',  # Adjust this path
            'file_path': os.path.join(LOGGING_DIR, "api_requests.log"),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console', "request_file"],
            'level': 'INFO',  # Use 'DEBUG' for more detailed logs
            'propagate': True,
        },
        'request': {
            'handlers': ['request_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


