An implementation of DjangoRestFramework authentication with JSON Web Tokens authentication. Althought modified, is based on this very good tutorial https://thinkster.io/tutorials/django-json-api/authentication


md projectname

cd projectname


- Create & activate a virtual environment

    ...> python -m venv venv

    ...> venv\scripts\activate


- Install django and dependencies:

    (venv) ...> pip install django

    (venv) ...> pip install djangorestframework

    (venv) ...> pip install pyjwt


- Create & run project

    (venv) ...> django-admin startproject apps

    (venv) ...apps> python manage.py runserver


- Create application

    (venv) ...apps> python manage.py startapp users

    (add it in INSTALLED_APPS in settings.py)


- Request - Response procedure

    Client request > urls.py > backends.py > views.py > serializers.py > models.py...

        (when error raises > expecptions.py)

    ...models.py > serializers.py > renderers.py > Server response


- Update models in database

    (venv) ...apps> python manage.py makemigrations

    (update changes in models)


    (venv) ...apps> python manage.py makemigrations users

    (specify app name on first makemigrations of a new app)


    (venv) ...apps> python manage.py migrate

    (apply changes in database)


- Declare auth customizations in settings.py

    (enable custom model instead of default django.contrib.auth.models.User)

    AUTH_USER_MODEL = 'users.User'


    REST_FRAMEWORK = {

        (customize error handling)

        'EXCEPTION_HANDLER': 'apps.exceptions.core_exception_handler',

        'NON_FIELD_ERRORS_KEY': 'error',


        (define authentication backend to authenticate requests or not)

        'DEFAULT_AUTHENTICATION_CLASSES': (

            'apps.users.backends.JWTAuthentication',

        )

    }


- Create superuser

    (venv) ...apps> python manage.py createsuperuser


- Run python shell

    (venv) ...apps> python manage.py shell


    (venv) ...apps> python manage.py shell_plus

    (shell_plus automatically imports all models from apps in INSTALLED_APPS)


- Requests with curl

    - (venv) ...apps> curl -X POST http://localhost:8000/users/signup/

    -H "Content-Type: application/json"

    -d {\"user\":{\"username\":\"john\",\"password\":\"12345678\",

    \"email\":\"test@email.net\"}}
    

    - (response) {"user": {"email": "test@email.net", "username": "john",

    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.

    eyJpZCI6MiwiZXhwaXJhdGlvbiI6MTU2OTY2MTY5MS45NDI4ODd9.

    mKg17j9ohqngz5FTME1s5__YjVuHRTpezG_Ox6eVPsk"}}


    - (venv) ...apps> curl -X POST http://localhost:8000/users/signin/ 
     
    -H "Content-Type: application/json" 
     
    -d {\"user\":{\"username\":\"john\",\"password\":\"12345678\"}}


    - (response) {"user": {"email": "test@email.net", "username": "john", 
    
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.
    
    eyJpZCI6MiwiZXhwaXJhdGlvbiI6MTU2OTY3MjY0MC40NjMxODJ9.
    
    vjQvyVQmwwDWBMqHfudUwxmaTkL3Lm2b45CJlQfG_v0"}}


    - (venv) ...apps> curl -X POST http://localhost:8000/users/update_current/
    
    -H "Content-Type: application/json" 
    
    -H "Authorization: Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9. 

    eyJpZCI6MiwiZXhwaXJhdGlvbiI6MTU2OTY3MjY0MC40NjMxODJ9.
    
    vjQvyVQmwwDWBMqHfudUwxmaTkL3Lm2b45CJlQfG_v0"
    
    -d {\"user\":{\"username\":\"john\",\"email\":\"modified@email.net\"}}
    

    - (response) {"user": {"email": "modified@email.net", "username": "john", 
    
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.
    
    eyJpZCI6MiwiZXhwaXJhdGlvbiI6MTU2OTY3MjU5Ni40NDA4MTd9.
    
    ms__6F5WdofIlHTgP9I2pJFg-60n1hPQNwWYJhYj05A"}}
