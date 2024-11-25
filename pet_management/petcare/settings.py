import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Static files configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Optional if you have a 'static/' folder

# Installed apps, including Django defaults and your app
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'petcareapp',  # Ensure the app name matches your actual app
]

# Debug mode (set to False in production)
DEBUG = True

# Secret key for Django (keep this secret in production)
SECRET_KEY = '5&#6rs$5rl356gx#c*h$4p@cz3a$o7wgc+e4b5myt)b6i8lyjn'

# Allowed hosts (add domain names in production)
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# URL configuration module
ROOT_URLCONF = 'petcare.urls'  # Ensure this matches your project folder name

# Middleware for request/response processing
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS
CSRF_USE_SESSIONS = True
# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Ensure this points to the right directory
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

# Database configuration (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pets',  # Ensure this database exists in PostgreSQL
        'USER': 'postgres',  # Ensure this user exists and has the required privileges
        'PASSWORD': 'agnes',  # Ensure this password is correct
        'HOST': 'localhost',  # Adjust if using a different host
        'PORT': '5432',  # Default PostgreSQL port
    }
}

# WSGI application
WSGI_APPLICATION = 'petcare.wsgi.application'

# Authentication settings
LOGIN_URL = 'login'  # Redirect to this page for unauthenticated users
LOGIN_REDIRECT_URL = 'home'  # Redirect after successful login

# Internationalization (adjust as needed)
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
