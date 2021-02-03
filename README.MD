# Mess management Server

An API server for the Mess Management System built with Django web framework. 
The API endpoints can currently be accessed at http://ec2-3-23-96-26.us-east-2.compute.amazonaws.com:8000/api/v1/

The available endpoints and API documentation can be accessed at http://ec2-3-23-96-26.us-east-2.compute.amazonaws.com:8000/api/swagger/
or http://ec2-3-23-96-26.us-east-2.compute.amazonaws.com:8000/api/redoc/

The current deployment is for development purposes. Debug is set to to True.
Please don't destroy my AWS.

Currently Implemented Features 
=
- User Registration
- User Login & Logout
- User password change

How To Use
=
## Clone project & Install Requirements
> Make sure you have already installed python3.
```
$ git clone https://github.com/prasunka/mess-management-server && cd mess-management-server
$ pip install pipenv
$ pipenv shell
$ pipenv install
```
## Setup database (PostgreSQL)
> For debian based systems
```
$ sudo apt install postgresql
$ sudo -u postgres createuser --interactive
Enter your username which is same as of your OS and press 'y' to make it superuser.

$ createdb <username>
$ psql (verify if you can login to postgres without a password)

$ createdb mess_management
```
## Setup environment variables
> Edit `config/.env.sample` file and add a random secret key. 
>
> Rename the file to .env

## Migrate data models
```
$ python3 manage.py migrate
```
## Create Admin User
```
$ python manage.py createsuperuser
```
## Run Tests
```
$ python manage.py test
```
## Run Server
```
$ python manage.py runserver
```
> Enter your browser http://localhost:8000/. You can login via admin in http://localhost:8000/admin/.

Documentation
=
Visit http://localhost:8000/swagger/ for swagger endpoint or http://localhost:8000/redoc/ for redoc endpoint.

TODOS
=
- ...
