IMPORT_EXPORT_USE_TRANSACTIONS = True

AUTHENTICATION_BACKENDS = [
    # 'django.contrib.auth.backends.ModelBackend',
    'backend.baseapp.backend.AdminBackend',
    'backend.teacher.backend.TeacherBackend',
]