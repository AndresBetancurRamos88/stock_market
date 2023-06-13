# stock_market
API stock market query by symbol

## Project Description
```
This project is an api to reuest stock markets base in a symbol that represents the market (Symbol = META):
```

## Technologies Used
```
- Python
- Django
- Django Rest framework
```

## Getting Started
```
Clone this repository 
- git clone https://github.com/AndresBetancurRamos88/stock_market

```

### Run project locally
```
Use the docker image to create the other containers with docker-compose
create the following .env files:
    - .env-db: contains the parameters for the connection to the database
        DB_USER=postgres
        DB_PASSWORD=postgres
        DB_NAME=db_name
        DB_HOST=db_host
        DB_PORT=5432

    - .env-django: contains the secrete key that each django project create 
        SECRET_KEY=django_key

    -it is requerired a postgresql data base to run the aplication or just replace de "DATABASES" parameter ( it is located in this path: ./stock_market/settings.py) for this:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }

Then run the following commands:
    - pip install pipenv
    - pipenv --python 3.9
    - pipenv shell
    - pipenv install
    - python manage.py migrate
    - python manage.py createsuperuser (create an user if you want to use dajngo admin panel)
    - python manage.py runserver

Go to the folowing url to test the API:
    http://127.0.0.1:8000/docs/

First use th signup API and keep the key response to request stock market API.

To test stock market API, take previously generated key put it into headers and put a symbol in parameters.
```