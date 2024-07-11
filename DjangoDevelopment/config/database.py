# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

from DjangoDevelopment.config.environ import env,BASE_DIR

if env('DATABASE')=='mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.'+env('DATABASE'),
            'HOST': env('DATABASE_HOST'),
            'PORT': env('DATABASE_PORT'),
            'NAME': env('DATABASE_NAME'),
            'USER': env('DATABASE_USER'),
            'PASSWORD': env('DATABASE_PASSWORD'),
        }
    }
elif env('DATABASE')=='postgresql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.'+env('DATABASE'),
            'HOST': env('DATABASE_HOST'),
            'PORT': env('DATABASE_PORT'),
            'NAME': env('DATABASE_NAME'),
            'USER': env('DATABASE_USER'),
            'PASSWORD': env('DATABASE_PASSWORD'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }