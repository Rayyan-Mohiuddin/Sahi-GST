import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = os.getenv('DEBUG', '0') == '1'
SECRET_KEY = os.getenv('SECRET_KEY', '')
if not SECRET_KEY:
    if not DEBUG and not os.getenv('TESTING'):
        raise RuntimeError('Set SECRET_KEY (or DEBUG=1 for local development).')
    SECRET_KEY = 'local-development-only-sahi-gst-do-not-deploy'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,testserver').split(',')
if os.getenv('RENDER_EXTERNAL_HOSTNAME'):
    ALLOWED_HOSTS.append(os.environ['RENDER_EXTERNAL_HOSTNAME'])
for name in ['VERCEL_URL', 'VERCEL_PROJECT_PRODUCTION_URL']:
    if os.getenv(name): ALLOWED_HOSTS.append(os.environ[name])
INSTALLED_APPS = ['django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles', 'allauth', 'allauth.account', 'invoices']
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware', 'whitenoise.middleware.WhiteNoiseMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware', 'allauth.account.middleware.AccountMiddleware', 'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF = 'config.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [BASE_DIR / 'templates'], 'APP_DIRS': True, 'OPTIONS': {'context_processors': ['django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION = 'config.wsgi.application'
if os.getenv('DATABASE_URL'):
    DATABASES = {'default': dj_database_url.parse(os.environ['DATABASE_URL'], conn_max_age=60)}
elif os.getenv('DEV_SQLITE') == '1' or os.getenv('TESTING'):
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'dev.sqlite3'}}
else:
    raise RuntimeError('PostgreSQL DATABASE_URL is required. DEV_SQLITE=1 is only for local smoke testing.')
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend', 'allauth.account.auth_backends.AuthenticationBackend']
AUTH_PASSWORD_VALIDATORS = [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}, {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}, {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}, {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}]
ACCOUNT_LOGIN_METHODS = {'username'}
ACCOUNT_SIGNUP_FIELDS = ['username*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'none'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
LANGUAGE_CODE = 'en-in'
TIME_ZONE = 'Asia/Kolkata'
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CSRF_TRUSTED_ORIGINS = [x for x in os.getenv('CSRF_TRUSTED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000').split(',') if x]
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-3.8-flash')
GEMINI_FREE_TIER_CONFIRMED = os.getenv('GEMINI_FREE_TIER_CONFIRMED', '0') == '1'
FRONTEND_DIR = BASE_DIR.parent / 'frontend' / 'out'
