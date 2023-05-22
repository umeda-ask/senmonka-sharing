senmonka-sharing
====

https://senmonka01.herokuapp.com/

## Requirement

python v ==3.11.3

```
Django==2.1.1
django-crispy-forms==1.7.2
django-filter==2.0.0
pytz==2018.5
```

argon2-cffi==21.3.0
argon2-cffi-bindings==21.2.0
asgiref==3.6.0
bcrypt==4.0.1
dj-database-url==1.3.0
Django==4.2
django-filter==2.0.0
django-heroku==0.3.1
gunicorn==20.1.0
Pillow==9.5.0
psycopg2==2.9.6
pycparser==2.21
pytz==2023.3
sqlparse==0.4.3
typing_extensions==4.5.0
tzdata==2023.3
whitenoise==6.4.0

## Usage

Steps

1. Git clone this project
2. Edit modelfile `app/models.py`
3. Run `makemigrations` and `migrate`
4. Edit HTML files `templates/item_filter.html` and `item_detail_contents.html`

If you use it production environment, you must replace `settings.SECRET_KEY`.

## Contribution

I wrote this for Japanese python beginners.

I would appreciate if you clone this project and replace japanese code with your language for your country's python beginners.

## Licence

[WTFPL](http://www.wtfpl.net/txt/copying/)

## Author

Kawase Tomohiro
