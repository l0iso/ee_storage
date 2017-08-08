DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ee_storage',
        'USER': 'admin',
        'PASSWORD': 'sqpl01-',
        'HOST': 'db.wiseweb.by',
        'PORT': '5432',
    }
}
