DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'db',
        'PORT': '3306',
        'TEST': {
            'NAME': 'blog_test',
        }
    }
}

DEBUG = True
