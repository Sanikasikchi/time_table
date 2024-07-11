# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

from pathlib import Path, os
from DjangoDevelopment.config.environ import BASE_DIR

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static/"),
    # os.path.join(BASE_DIR, "media/"),
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
