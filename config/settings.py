import os
import sentry_sdk
from django.conf import settings
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_8o_w#6@te08l)aewj@bk)3(m#oz63clh@fw#5!4s1%37re4b2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True   # True

ALLOWED_HOSTS = ['*', '127.0.0.1', 'localhost']

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'paystack.apps.PaystackConfig',
    # paystack app
    # 'paystack',
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.github',
    # 'store.apps.StoreConfig',  # store app shopping cart app, also print receipt
]

THIRD_PARTY_APPS = [
    'django_countries',
    'django_seed',
    'translation_manager',
    'storages',
    'tailwind',
    'theme',
    'tailwindcss',
    'django_browser_reload',
    'bootstrap_daterangepicker',
    'jquery',
    'social_django',
]

PROJECT_APPS = [
    'core.apps.CoreConfig',
    'users.apps.UsersConfig',
    'rooms.apps.RoomsConfig',
    'reviews.apps.ReviewsConfig',
    'reservations.apps.ReservationsConfig',
    'lists.apps.ListsConfig',
    'conversations.apps.ConversationsConfig',
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GITHUB_KEY = 'df6a5412a07f33314d1d'
SOCIAL_AUTH_GITHUB_SECRET = '574012c80fc95a3f23b5ebaf442e82aa5c896995'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'myapp.pipeline.load_user',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

# LOGIN_REDIRECT_URL = '/'

ROOT_URLCONF = 'config.urls'

PAYSTACK_PUBLIC_KEY = "puroshile2323"  # paystack public key
PAYSTACK_SECRET_KEY = "puroshile2323"  # paystack secret key

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',  # new
                'django.template.context_processors.media',  # new
                'django.template.context_processors.static',  # new
                'django.template.context_processors.csrf',  # new
                # 'app.paystack.context_processors.paystack', # paystack context processor
                # 'app.context_processors.paystack', # paystack context processor
                # 'allauth.account.context_processors.account',  # new
                # 'allauth.socialaccount.context_processors.socialaccount',  # new
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# if DEBUG:
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.sqlite3",
#             "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
#         }
#     }
# else:
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.postgresql",
#             "HOST": os.environ.get("RDS_HOST"),
#             "NAME": os.environ.get("RDS_NAME"),
#             "PASSWORD": os.environ.get("RDS_PASSWORD"),
#             "USER": os.environ.get("RDS_USER"),
#             "PORT": "5432",
#         }
#     }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

# Default languages
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

LOGIN_URL = 'users:login'

LOGIN_REDIRECT_URL = 'core:home'

LOGOUT_REDIRECT_URL = 'core:home'

# AWS S3

""" 
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

"""

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

# Email

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'mtorresl@uft.edu'
EMAIL_HOST_PASSWORD = 'Mario1579'
EMAIL_FROM = 'mtorresl@uft.edu'
EMAIL_USE_TLS = True  # new FUCKING headache!!!!!!!!!!!!!

# Locale
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

"""
# Languages
LANGUAGES = (
    ('en', _('English')),
    ('es', _('Spanish')),
)
"""

# Sentry

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_URL'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
    # ignore_errors=['django.security.DisallowedHost'],
)

sentry_sdk.integrations.logging.ignore_logger('django.security.DisallowedHost')

# tailwind APP THEME
TAILWIND_APP_NAME = 'theme'

INTERNAL_IPS = [
    '127.0.0.1',
]

# BASE_DIR = Path(__file__).resolve().parent

TAILWINDCSS_CLI_FILE = 'tailwindcss-linux-x64'
TAILWINDCSS_CONFIG_FILE = os.path.join('tailwind.config.js')

# TAILWINDCSS_CONFIG_FILE = BASE_DIR / "tailwind.config.js'


# For file mode
TAILWINDCSS_OUTPUT_FILE = 'style.css'
