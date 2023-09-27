from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
DEBUG = True

# ALLOWED_HOSTS = ['http://127.0.0.1:8000/']
ALLOWED_HOSTS = ['127.0.0.1']


# Application definition


# GOOGLE SITE ID
SITE_ID=4


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'userarea.apps.UserareaConfig',
    'useronboard.apps.UseronboardConfig',
    'django_countries',
    'staffapp.apps.StaffappConfig',
    # 
    
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

]


# # IF I WAS TO USE DIFFERENT PROVIDES, I'LL LIST SIMILAR CODE BELOW FOR THAT PROVIDER.
SOCIALACCOUNT_PROVIDERS = {
    "google" : {
        "SCOPE" : [
            "profile",
            "email"
        ],
        "AUTH_PARAMS" : {"access_type" : "online"}
    }
}

# ALLUTH GOOGLE LOGIN UNTEGRATION FUNCTIONALITY CODES BELOW ENDS HERE

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django_auto_logout.middleware.auto_logout',
]
# SECURE_CROSS_ORIGIN_OPENER_POLICY = None

from datetime import timedelta
AUTO_LOGOUT = {
    'IDLE_TIME': timedelta(minutes=10),
    'Login': True,
}



ROOT_URLCONF = 'DHMSProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'Templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_auto_logout.context_processors.auto_logout_client',
            ],
        },
    },
]


# LOGIN REDIRECT
LOGIN_REDIRECT_URL = '/useronboard/login/'
LOGIN_URL='/useronboard/login/'
# 
# LOGOUT_REDIRECT_URL = '/'
# LOGIN_URL='/'

WSGI_APPLICATION = 'DHMSProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'dhms',
#         'USER': 'admin',
#         'PASSWORD': 'password'
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR / 'static')
]

STATIC_ROOT =os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SENDING EMAILS TO SHELL/CONSOLE
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# SENDING EMAILS WITH GMAIL
# EMAIL_HOST = str(os.getenv('EMAIL_HOST'))
# EMAIL_HOST_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = str(os.getenv('EMAIL_HOST_USER'))
# EMAIL_HOST_PASSWORD =  str(os.getenv('EMAIL_HOST_PASSWORD'))

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'dhmsinventoryapp@gmail.com'
EMAIL_HOST_PASSWORD = 'ffjsspjiqfvvbuxd'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False


# AUTH GOOGLE SIGNUP INTEGRATION FUNCTIONALITY CODES BELOW STARTS HERE

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',   
]

