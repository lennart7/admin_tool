# config production db for heroku
DATABASES['default'] = dj_database_url.config()

ALLOWED_HOSTS = ['obscure-eyrie-90249.herokuapp.com']
