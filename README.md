# blog

## Features

- Django 2.0+
- Uses [Docker](https://www.docker.com/)
- MySQL database support with PyMySQL.
- Images save on [cloudinary](https://cloudinary.com/)
- Application is running on heroku.
- Use scss to write style.
- Use whitenoise to manage static files.


## Deployment

It is possible to deploy to Heroku or to your own server.

### Heroku

```bash
$ heroku create
$ heroku addons:add cleardb -a [appname]
$ heroku container:push web -a [appname]
$ heroku container:release web -a [appname]
$ heroku run python manage.py makemigrations -a [appname]
$ heroku run python manage.py migrate -a [appname]
$ heroku run python manage.py collectstatic -a [appname]
$ heroku open -a [appname]
```

## Getting Started

First clone the repository from Github:
```bash
$ git clone git@github.com:nonobu722/blog.git
$ cd blog
```

Start docker container with deamon.
```bash
$ docker-compose up -d  
```

Add SECRET_KEY to secret_settings.py
```bash
$ docker-compose run web python ./mysite/generate_secretkey_setting.py > ./src/mysite/secret_settings.py
```

Add CLOUDINARY_STORAGE and DATABASES to secret_settings.py.
Template is below and Variables need to replace. 
```
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'name',
    'API_KEY': 'api_key',
    'API_SECRET': 'secret'
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dbname',
        'USER': 'dbuser',
        'PASSWORD': 'dbpass',
        'HOST': 'dbhost',
        'PORT': 'dbport',
    }
}
```

Migrate db.
```bash
$ docker-compose run web ./manage.py makemigrations
$ docker-compose run web ./manage.py migrate
$ docker-compose run web ./manage.py collectstatic
```
