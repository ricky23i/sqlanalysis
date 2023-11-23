from django.core.management.utils import get_random_secret_key
import os

SECRET_KEY = get_random_secret_key()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
INSTALLED_APPS = [
    # ...
    'corsheaders',
    # ...
]

MIDDLEWARE = [
    # ...
    'corsheaders.middleware.CorsMiddleware',
    # ...
]

CORS_ALLOWED_ORIGINS = [
    'http://sqlanalysis.s3-website.us-east-2.amazonaws.com', 
]

ALLOWED_HOSTS = ['*']
ROOT_URLCONF = 'myapi.urls'