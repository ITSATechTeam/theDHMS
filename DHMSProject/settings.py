
# ------------------------------

from pathlib import Path
import os
# from dotenv import load_dotenv
# load_dotenv()

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

# AZURE AD ACTIVATION CODE STARTS HERE
from ms_identity_web.configuration import AADConfig
from ms_identity_web import IdentityWebPython


# for rendering 401 or other errors from msal_middleware
# MIDDLEWARE.append('ms_identity_web.django.middleware.MsalMiddleware')



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = str(os.getenv('DEBUG'))
# DEBUG = str(os.getenv('DEBUG')) == 'True'
DEBUG = True

CSRF_FAILURE_VIEW = 'useronboard.views.csrf_failure'


# ALLOWED_HOSTS = ['http://127.0.0.1:8000/']
ALLOWED_HOSTS = ['*']

AXES_RESET_COOL_OFF_ON_FAILURE_DURING_LOCKOUT = False
AXES_LOCKOUT_CALLABLE = "staffapp.views.lockout"
AXES_FAILURE_LIMIT = 7
AXES_COOLOFF_TIME = 1
AXES_RESET_ON_SUCCESS = True


# Application definition


# SECURE_HSTS_SECONDS = 518400
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

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
    'dhmsapiapp.apps.DhmsapiappConfig',
    'aichat.apps.AichatConfig',
    'rest_framework',
    'rest_framework.authtoken',
    
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
    'pwa',
    'axes',
]



# # IF I WAS TO USE DIFFERENT PROVIDES, I'LL LIST SIMILAR CODE BELOW FOR THAT PROVIDER.
SOCIALACCOUNT_PROVIDERS = {
    "google" : {
        'APP': {
            'client_id': '724544088417-prffhjnn8rd2b0nj2r5ia1br69madgou.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        },
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



# FB APP IS = 334644112749247
# FB APP SECRET KEY = ca22f180cd84bd443451de696b89e1d5
# DISPLAY NAME = Family DHMS - Test1

#facebook
SOCIAL_AUTH_FACEBOOK_KEY = '2091141407903994'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET ='59dbe7831f34b6a5ba802a8231317683'



# AUTH GOOGLE SIGNUP INTEGRATION FUNCTIONALITY CODES BELOW STARTS HERE
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',  
    # 
    # 'django_python3_ldap.auth.LDAPBackend',
]

# REST_FRAMEWORK = {
#     # Use Django's standard `django.contrib.auth` permissions,
#     # or allow read-only access for unauthenticated users.
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
#     ]
# }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    ],
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ],
}

# TOKEN_EXPIRED_AFTER_SECONDS = 86400



SOCIALACCOUNT_AUTO_SIGNUP = False
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'


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
    # 
    'django_user_agents.middleware.UserAgentMiddleware',
    # 
    'allauth.account.middleware.AccountMiddleware',
    # 'csp.middleware.CSPMiddleware'


    # Below middleware should always be the last
    'axes.middleware.AxesMiddleware',
]



AAD_CONFIG = AADConfig.parse_json(file_path='aad.config.json')
MS_IDENTITY_WEB = IdentityWebPython(AAD_CONFIG)
MIDDLEWARE.append('ms_identity_web.django.middleware.MsalMiddleware')
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
            BASE_DIR / 'templates'
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


# WSGI_APPLICATION = 'DHMSProject.wsgi.application'
# WSGI_APPLICATION = 'wsgi.application'

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



# AWS S3 Configuration starts here
AWS_ACCESS_KEY_ID = "AKIAQRVIHB6EPQLTI3SL"
AWS_SECRET_ACCESS_KEY = str(os.getenv('AWS_SECRET_ACCESS_KEY'))

# Your app endpoint
# AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL')  

# Only public read for now
AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL='public-read'

AWS_STORAGE_BUCKET_NAME = 'dhmsimages'

AWS_S3_FILE_OVERWRITE = False

# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS S3 Configuration ends here





# CSP SECURITY CODE IMPLEMENTATION STARTS HERE

# uri to report policy violations
# uri to report policy violations
CSP_REPORT_URI = '<add your reporting uri>'

# default source as self
CSP_DEFAULT_SRC = ("'self', 'STATIC_URL'", )
# CSP_DEFAULT_SRC = ("'self'", )

# style from our domain and bootstrapcdn
# CSP_STYLE_SRC = ("'self'", 
# 	"stackpath.bootstrapcdn.com")

# scripts from our domain and other domains
CSP_SCRIPT_SRC = ("'self'", 
	"www.google-analytics.com", 
	"ssl.google-analytics.com", 
	# "cdn.ampproject.org", 
	"www.googletagservices.com", 
	# "pagead2.googlesyndication.com"
    )

# images from our domain and other domains
CSP_IMG_SRC = ("'self'", 
	# "www.google-analytics.com", 
	# "raw.githubusercontent.com", 
	# "googleads.g.doubleclick.net"
    )

# loading manifest, workers, frames, etc
CSP_FONT_SRC = ("'self'", )
CSP_CONNECT_SRC = ("'self'", 
	# "www.google-analytics.com"
      )
CSP_OBJECT_SRC = ("'self'", )
CSP_BASE_URI = ("'self'", )
CSP_FRAME_ANCESTORS = ("'self'", )
CSP_FORM_ACTION = ("'self'", )
CSP_INCLUDE_NONCE_IN = ('script-src', )
CSP_MANIFEST_SRC = ("'self'", )
CSP_WORKER_SRC = ("'self'", )
CSP_MEDIA_SRC = ("'self'", )


# CSP SECURITY CODE IMPLEMENTATION ENDS HERE