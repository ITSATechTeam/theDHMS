from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# PWA SETTINGS STARTS HERE
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'static/js/', 'serviceworker.js')

# MANIFEST.JSON DETAILS
PWA_APP_NAME = 'DHMS'
PWA_APP_DESCRIPTION = "DHMS PWA"
PWA_APP_THEME_COLOR = '#2A66B0'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
	{
		'src': 'static/onboard/img/12by12icon.png',
		'sizes': '48x48'
	},
	{
		'src': 'static/onboard/img/72by72icon.png',
		'sizes': '144x144'
	},
	{
		'src': 'static/onboard/img/98by98icon.png',
		'sizes': '196x196'
	}
]
PWA_APP_ICONS_APPLE = [
	{
		'src': 'static/onboard/img/28by28appleicon.png',
		'sizes': '27.5x27.5'
	}
]
PWA_APP_SPLASH_SCREEN = [
	{
		'src': 'static/Home/img/dhmspwasplashscreen1.PNG',
		'src': 'static/Home/img/dhmspwasplashscreendesktop.PNG',
		# 'src': 'static/general/img/itsalogopng1.PNG',
		'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
	}
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'

# PWA SETTNGS ENDS HERE

# AZURE AD ACTIVATION CODE STARTS HERE\
from ms_identity_web.configuration import AADConfig
from ms_identity_web import IdentityWebPython


# for rendering 401 or other errors from msal_middleware
# MIDDLEWARE.append('ms_identity_web.django.middleware.MsalMiddleware')



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
DEBUG = True

# ALLOWED_HOSTS = ['http://127.0.0.1:8000/']
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Application definition


# GOOGLE SITE ID
SITE_ID=5


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
    'familydhmsapp.apps.FamilydhmsappConfig',
    'dhmsadminboard.apps.DhmsadminboardConfig',
    # 
    
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    # 
    # 'django_python3_ldap',
    'django_user_agents',
    # 
    'storages',
    'pwa'
]


# # IF I WAS TO USE DIFFERENT PROVIDES, I'LL LIST SIMILAR CODE BELOW FOR THAT PROVIDER.
SOCIALACCOUNT_PROVIDERS = {
    "google" : {
        "SCOPE" : [
            "profile",
            "email"
        ],
        "AUTH_PARAMS" : {"access_type" : "online"}
    },

    'facebook':
       {'METHOD': 'oauth2',
        'SCOPE': ['email','public_profile'],
        # 'SCOPE': ['email','public_profile', 'user_friends'],
        'APP': {
            'client_id': '2091141407903994',
            'secret': '59dbe7831f34b6a5ba802a8231317683',
        },
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time'],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v13.0',
        'GRAPH_API_URL': 'https://graph.facebook.com/v13.0',
       }
}

SOCIALACCOUNT_AUTO_SIGNUP = False
ACCOUNT_EMAIL_VERIFICATION = 'none'



# FB APP IS = 334644112749247
# FB APP SECRET KEY = ca22f180cd84bd443451de696b89e1d5
# DISPLAY NAME = Family DHMS - Test1

#facebook
SOCIAL_AUTH_FACEBOOK_KEY = '2091141407903994'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET ='59dbe7831f34b6a5ba802a8231317683'


# ALLUTH GOOGLE LOGIN UNTEGRATION FUNCTIONALITY CODES BELOW ENDS HERE


# SOCIALACCOUNT_PROVIDERS = \
#     {'facebook':
#        {'METHOD': 'oauth2',
#         'SCOPE': ['email','public_profile', 'user_friends'],
#         'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
#         'FIELDS': [
#             'id',
#             'email',
#             'name',
#             'first_name',
#             'last_name',
#             'verified',
#             'locale',
#             'timezone',
#             'link',
#             'gender',
#             'updated_time'],
#         'EXCHANGE_TOKEN': True,
#         'LOCALE_FUNC': lambda request: 'kr_KR',
#         'VERIFIED_EMAIL': False,
#         'VERSION': 'v2.4'}}

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
    # 
    'django_user_agents.middleware.UserAgentMiddleware'
]


MIDDLEWARE.append('ms_identity_web.django.middleware.MsalMiddleware')
AAD_CONFIG = AADConfig.parse_json(file_path='aad.config.json')
MS_IDENTITY_WEB = IdentityWebPython(AAD_CONFIG)
ERROR_TEMPLATE = 'auth/{}.html' 

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
    # 
    'django_python3_ldap.auth.LDAPBackend',
]


# AWS S3 Configuration starts here
AWS_ACCESS_KEY_ID = "AKIAQRVIHB6EPQLTI3SL"
AWS_SECRET_ACCESS_KEY = "ZLCrN68pLrtK+/wvMD+g15p8aFsjRYD7OzxdkLhA"

# Your app endpoint
# AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL')  

# Only public read for now
AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL='public-read'

AWS_STORAGE_BUCKET_NAME = 'dhmsimages'

AWS_S3_FILE_OVERWRITE = False

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS S3 Configuration ends here






# LDAP SETTINGS RECOMMENDATION STARTS HERE
# The URL of the LDAP server(s).  List multiple servers for high availability ServerPool connection.
LDAP_AUTH_URL = ["ldap://localhost:389"]

# Initiate TLS on connection.
LDAP_AUTH_USE_TLS = False

# Specify which TLS version to use (Python 3.10 requires TLSv1 or higher)
import ssl
LDAP_AUTH_TLS_VERSION = ssl.PROTOCOL_TLSv1_2

# The LDAP search base for looking up users.
LDAP_AUTH_SEARCH_BASE = "ou=people,dc=example,dc=com"

# The LDAP class that represents a user.
LDAP_AUTH_OBJECT_CLASS = "inetOrgPerson"

# User model fields mapped to the LDAP
# attributes that represent them.
# LDAP_AUTH_USER_FIELDS = {
#     "username": "uid",
#     "first_name": "givenName",
#     "last_name": "sn",
#     "email": "mail",
# }

# Depending on how your Active Directory server is configured, the following additional settings 
# may match your server better than the defaults used by django-python3-ldap:

LDAP_AUTH_USER_FIELDS = {
    "username": "sAMAccountName",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}

LDAP_AUTH_OBJECT_CLASS = "user"



# A tuple of django model fields used to uniquely identify a user.
LDAP_AUTH_USER_LOOKUP_FIELDS = ("username",)

# Path to a callable that takes a dict of {model_field_name: value},
# returning a dict of clean model data.
# Use this to customize how data loaded from LDAP is saved to the User model.
LDAP_AUTH_CLEAN_USER_DATA = "django_python3_ldap.utils.clean_user_data"

# Path to a callable that takes a user model, a dict of {ldap_field_name: [value]}
# a LDAP connection object (to allow further lookups), and saves any additional
# user relationships based on the LDAP data.
# Use this to customize how data loaded from LDAP is saved to User model relations.
# For customizing non-related User model fields, use LDAP_AUTH_CLEAN_USER_DATA.
LDAP_AUTH_SYNC_USER_RELATIONS = "django_python3_ldap.utils.sync_user_relations"

# Path to a callable that takes a dict of {ldap_field_name: value},
# returning a list of [ldap_search_filter]. The search filters will then be AND'd
# together when creating the final search filter.
LDAP_AUTH_FORMAT_SEARCH_FILTERS = "django_python3_ldap.utils.format_search_filters"

# Path to a callable that takes a dict of {model_field_name: value}, and returns
# a string of the username to bind to the LDAP server.
# Use this to support different types of LDAP server.
# LDAP_AUTH_FORMAT_USERNAME = "django_python3_ldap.utils.format_username_openldap"
# for MS AD
LDAP_AUTH_FORMAT_USERNAME = "django_python3_ldap.utils.format_username_active_directory"

# Sets the login domain for Active Directory users.
# LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = None
# for MS AD
LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = "DOMAIN"

# For user-principal-name formats (e.g. “user@domain.com”):
LDAP_AUTH_FORMAT_USERNAME = "django_python3_ldap.utils.format_username_active_directory_principal"
LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = "domain.com"

# The LDAP username and password of a user for querying the LDAP database for user
# details. If None, then the authenticated user will be used for querying, and
# the `ldap_sync_users`, `ldap_clean_users` commands will perform an anonymous query.
LDAP_AUTH_CONNECTION_USERNAME = None
LDAP_AUTH_CONNECTION_PASSWORD = None

# Set connection/receive timeouts (in seconds) on the underlying `ldap3` library.
LDAP_AUTH_CONNECT_TIMEOUT = None
LDAP_AUTH_RECEIVE_TIMEOUT = None

# 
