import os
from os import environ, path
from os.path import join, dirname
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

# Load environment variables
env_path = join(dirname(__file__), ".env")
load_dotenv(env_path)


BUILD_VERSION = environ.get("BUILD_VERSION") or ""


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
    "corsheaders",
    "django_filters",
    "import_export",
    "open_problems",
    "posts_comments",
    "annotations",
    "references",
    "core",
    "users",
    "reports",
    "categories",
]
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
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


REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "core.exception_handler.custom_exception_handler",
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
}

ROOT_URLCONF = "OPL.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            str(cwd_path.joinpath("templates")),
            str(cwd_path.joinpath(BASE_DIR, "templates")),
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
    },
    "test": {"NAME": f"test_{environ.get('DB_NAME')}"},
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache_backends",
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
    "https://longevityknowledge.app",
    "http://localhost:8000",
    "http://127.0.0.1",
]

ALLOWED_HOSTS = ["*"]

## AZURE IDS
AZURE_TENANT_ID = environ.get("AZURE_TENANT_ID")
AZURE_CLIENT_ID = environ.get("AZURE_CLIENT_ID")

# EMAIL BACKENDS - MAILTRAP
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "live.smtp.mailtrap.io"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = "2525"

MAILTRAP_API_KEY = os.environ.get("MAILTRAP_API_KEY")
MAILTRAP_SENDER = os.environ.get("MAILTRAP_SENDER")
