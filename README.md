# p8-purbeurre
"Le gras, c'est la vie."

This application offers higher or equivalent quality replacement products and to register them in your personal account.

## Requirements :

- python3
- postgresql 
- pip3
```
pip install -r requirements.txt
```

## How to use ( for testing only )

Configure your database access variables in .env file :
```bash
DB_NAME="YOUR_DATABASE_NAME"
DB_USER="YOUR_DATABASE_USER"
DB_PASSWORD="YOUR_DATABASE_PASSWORD"
DB_HOST="YOUR_SERVER_IP"
DB_PORT="5432"
```
Export your .env file in your environment :
```bash
$ export $(cat .env | xargs)
```

Set DEBUG to True in settings file
```python
DEBUG = True
```
Import some  products in your database from OpenFoodFacts
ex : 10 categories and 5 products in each category which makes a total of 50 products imported.
```bash
$ cd purbeurre
$ python manage.py import -c 10 -p 5
```
For more info :
```bash
$ python manage.py import -h
```
Start the app :
```bash
$ python manage.py runserver
```
