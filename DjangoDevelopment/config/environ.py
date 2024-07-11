from pathlib import Path, os
BASE_DIR = Path(__file__).resolve().parent.parent.parent
import environ
get_env = environ.Env()

# SECURITY WARNING: don't run with debug turned on in production!
# dev / prod / staging 
APP_ENV = 'dev'        

if APP_ENV=='prod':
    DEBUG = False
    environ.Env.read_env(os.path.join(BASE_DIR, 'production.env'))
elif APP_ENV=='staging':
    DEBUG = True
    environ.Env.read_env(os.path.join(BASE_DIR, 'staging.env'))
else:
    DEBUG = True
    environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

def env(var_name):
    try:
        return get_env(var_name)
    except:
        return ''
        return None

ALLOWED_HOSTS = ['localhost','127.0.0.1','192.168.10.102','svikapos.com']
