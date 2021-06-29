"""
Настройки редактора ckeditor.
"""
CKEDITOR_UPLOAD_PATH = "ckeditor/uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'toolbar': 'full',
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
