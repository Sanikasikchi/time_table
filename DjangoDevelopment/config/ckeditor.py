# https://pypi.org/project/django-ckeditor/
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "uploads/ckeditor"
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
                'extraPlugins': ','.join([
                    'uploadimage',  # the upload image feature
                    # your extra plugins here
                    'div',
                    # 'image', 
                    # 'image2',
                    'autolink',
                    'autoembed',
                    'embedsemantic',
                    'autogrow',
                    # 'devtools',
                    'widget',
                    'lineutils',
                    'clipboard',
                    'dialog',
                    'dialogui',
                    'elementspath'
                ]),
    },
}
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_UPLOAD_SLUGIFY_FILENAME = False
