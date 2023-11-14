from os import environ
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BUILD_VERSION = environ.get("BUILD_VERSION")

match (environ.get("WEB_API_URLS")):
    case str(value):
        web_api_urls = value.split("|")
    case _:
        web_api_urls = []

match (environ.get("SPA_URLS")):
    case str(value):
        spa_urls = value.split("|")
    case _:
        spa_urls = []

match (environ.get("DEBUG_MODE")):
    case str(value):
        debug_mode = value.lower() == "true"
    case _:
        debug_mode = []

cwd_path = Path.cwd()

SECRET_KEY = environ.get("SECRET_KEY")

cwd_path = Path.cwd()

SECRET_KEY = environ.get("SECRET_KEY")
DEBUG = debug_mode
INSTALLED_APPS = [
    "drf_yasg",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "open_problems",
    "posts_comments",
    "annotations",
    "corsheaders",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://dev.longevityknowledge.app",
    "https://longevityknowledge.app",
    "http://127.0.0.1",
    "https://localhost:8000",
]

REST_FRAMEWORK = {"DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"]}
ROOT_URLCONF = "OPL.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            str(cwd_path.joinpath("templates")),
            str(cwd_path.joinpath("questions", "templates")),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
WSGI_APPLICATION = "OPL.wsgi.application"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": environ.get("DB_NAME"),
        "USER": environ.get("DB_USER"),
        "PASSWORD": environ.get("DB_PASSWORD"),
        "HOST": environ.get("DB_HOST"),
        "PORT": environ.get("DB_PORT"),
    }
}
STATIC_URL = "api/static/"
STATIC_ROOT = str(cwd_path.joinpath("staticfiles"))
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = "/api/static/"
STATIC_ROOT = str(cwd_path.joinpath("staticfiles"))

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Set 'SECURE_PROXY_SSL_HEADER' to tell Django that the connection is HTTPS even if it's forwarded by a proxy.
# http_protocol = configuration['settings']['httpProtocol']
http_protocol = environ.get("HTTP_PROTOCOL")
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", http_protocol)

# Set 'SESSION_COOKIE_SECURE' and 'CSRF_COOKIE_SECURE' to True to ensure cookies are only sent over HTTPS.
session_cookie_secure = environ.get("SESSION_COOKIE_SECURE")
csrf_cookie_secure = environ.get("CSRF_COOKIE_SECURE")
SESSION_COOKIE_SECURE = session_cookie_secure
CSRF_COOKIE_SECURE = csrf_cookie_secure
session_cookie_domain = environ.get("SESSION_COOKIE_DOMAIN")
SESSION_COOKIE_DOMAIN = session_cookie_domain

CSRF_TRUSTED_ORIGINS = [
    "https://dev.longevityknowledge.app",
    "https://dev-api.longevityknowledge.app",
    "https://admin.longevityknowledge.app",
    "http://localhost:8000",
    "http://127.0.0.1",
]

ALLOWED_HOSTS = ["*"]
