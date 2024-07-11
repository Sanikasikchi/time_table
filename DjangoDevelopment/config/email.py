from DjangoDevelopment.config.environ import env,BASE_DIR

ADMIN_EMAIL = env('ADMIN_EMAIL')

EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

if env('MAIL_ENCRYPTION') == 'ssl':
    EMAIL_USE_SSL = True
else:   
    EMAIL_USE_TLS = True
