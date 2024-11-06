"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
from datetime import timedelta
from pathlib import Path
import environ

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False)
)

# Take environment variables from .env file
environ.Env.read_env()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@e^i8h4!7nvuw(p5=$mvf!j0jali=twlh4*^%=0a82kz+o-p9a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'accounts',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'drf_spectacular',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    },
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'accounts.User'

# django-allauth
SITE_ID = 1 # 해당 도메인 id
ACCOUNT_UNIQUE_EMAIL = True # User email unique 사용 여부
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username' # 사용자 이름 필드 지정
ACCOUNT_USERNAME_REQUIRED = True # User username 필수 여부
ACCOUNT_EMAIL_REQUIRED = True # User email 필수 여부
ACCOUNT_AUTHENTICATION_METHOD = 'email' # 로그인 인증 수단
ACCOUNT_EMAIL_VERIFICATION = 'none' # email 인증 필수 여부

# Simple JWT 설정
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

REST_AUTH_SERIALIZERS = {
    'TOKEN_SERIALIZER': 'dj_rest_auth.serializers.JWTSerializer',
    
}

# Set SameSite to 'None' (for cross-origin requests) or 'Lax'/'Strict' as needed
JWT_AUTH_COOKIE_SAMESITE = 'None'  # Use 'None' for cross-origin requests
JWT_AUTH_REFRESH_COOKIE_SAMESITE = 'None'  # Same for refresh token

# Ensure the cookie is secure (for HTTPS) if SameSite=None is used
JWT_AUTH_COOKIE_SECURE = True  # True if using HTTPS, False for local development over HTTP
JWT_AUTH_REFRESH_COOKIE_SECURE = True  # Same for refresh token

REST_USE_JWT = True
REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'ft_transcendence-app-auth',
    'JWT_AUTH_REFRESH_COOKIE': 'ft_transcendence-app-refresh-token',
    'JWT_AUTH_HTTPONLY': True,
    'TOKEN_MODEL': None,
    'USER_DETAILS_SERIALIZER': 'accounts.serializers.CustomUserDetailsSerializer',
    'REGISTER_SERIALIZER': 'accounts.serializers.CustomRegisterSerializer',
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # 기본 백엔드
    # 추가적인 백엔드를 여기에 정의할 수 있습니다.
]
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = [
    "http://localhost:5173",
    "http://localhost:8000",
    'https://localhost',
    'https://127.0.0.1',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # front-end origin
    "http://localhost:8000",  # back-end origin
    "http://localhost:3000",  # front-end origin
    'https://localhost',
    'https://127.0.0.1',
]

CSRF_TRUSTED_ORIGINS = [
    'https://localhost',
    'https://127.0.0.1',
]

SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True  # 로컬 환경에서는 False, 배포 환경에서는 True로 설정

SOCIALACCOUNT_PROVIDERS = {
    'fortytwo': {
        'APP': {
            'client_id': env('MINSEPAR_CLIENT_ID'),
            'secret': env('MINSEPAR_SECRET'),
            'key': ''
        }
    },
}

# SOCIALACCOUNT_ADAPTER = 'accounts.adapter.FortyTwoAdapter'

# SOCIALACCOUNT_PROVIDERS = {
#     'fortytwo': {
#         'APP': {
#             'SCOPE': ['public'],  # Define the scopes needed (if applicable)
#             'AUTH_PARAMS': {},
#             'OAUTH2_ACCESS_TOKEN_URL': 'https://api.intra.42.fr/oauth/token',
#             'OAUTH2_AUTHORIZE_URL': 'https://api.intra.42.fr/oauth/authorize',
#             'OAUTH2_PROFILE_URL': 'https://api.intra.42.fr/v2/me',
#             'OAUTH2_CLIENT_ID': 'u-s4t2ud-f3c794a53848db3b102519cb5cd7123e14dae487ccdb02741f5ef3b8781504ef',
#             'OAUTH2_CLIENT_SECRET': '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',
#         }
#     }
# }
        # 'SCOPE': ['profile', 'email'],  # Define the scopes needed (if applicable)

        # 'OAUTH2_ACCESS_TOKEN_URL': 'https://api.intra.42.fr/oauth/token',
        # 'OAUTH2_AUTHORIZE_URL': 'https://api.intra.42.fr/oauth/authorize',
        # 'OAUTH2_PROFILE_URL': 'https://api.intra.42.fr/v2/me',
        # 'OAUTH2_CLIENT_ID': '<your-client-id>',
        # 'OAUTH2_CLIENT_SECRET': '<your-client-secret>',

# ACCOUNT_LOGIN_ON_GET = True
ACCOUNT_AUTHENTICATED_REDIRECT_URL = '/'  # or wherever you want them to go after logging in

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'api/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SPECTACULAR_SETTINGS = {
    'TITLE': 'Your Project API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'APPEND_PATHS': {
        '/api/v1/accounts/oauth2/fortytwo/login/': {
            'post': {
                'operationId': 'fortytwo_oauth2_login',
                'description': '42 OAuth2 로그인 엔드포인트입니다.'
                               '42 OAuth2 인증 URL로 리다이렉트합니다.'
                               'csrf token이 필요합니다.',
                'tags': ['Authentication'],
                'responses': {
                    '302': {
                        'description': 'Redirects to the 42 OAuth2 authorization URL.',
                    },
                },
            },
        },
    },
}

#logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # Disable existing loggers set by Django

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
        'console': {
            'level': 'INFO',  # Set the log level for this handler
            'class': 'logging.StreamHandler',  # Output to the console
            'formatter': 'simple',  # Use the simple formatter
        },
        'file': {
            'level': 'ERROR',  # Log error messages and above to file
            'class': 'logging.FileHandler',  # Write logs to a file
            'filename': 'django_errors.log',  # Log file location
            'formatter': 'verbose',  # Use the verbose formatter
        },
    },

    'loggers': {
        'django': {
            'handlers': ['console', 'file'],  # Use both console and file handlers
            'level': 'INFO',  # Log messages of level INFO and above
            'propagate': True,  # Propagate messages to higher level loggers
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR',  # Only log errors in request processing
            'propagate': False,  # Don't propagate to the 'django' logger
        },
        'django.security': {
            'handlers': ['file'],
            'level': 'WARNING',  # Log warnings related to security
            'propagate': False,  # Don't propagate to the 'django' logger
        },
        'accounts': {
            'handlers': ['console', 'file'],
            'level': 'INFO',  # You can adjust the log level for specific apps
            'propagate': False,
        },
    },
}