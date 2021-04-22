# Mess management Server

An API server for a Hostel Mess Management System built with Django web framework. 

For the React-Native client code, head over to this [repository](https://github.com/Prateek93a/NoMess).

**The available endpoints and API documentation can be accessed**:
[here](https://mess-management-server.herokuapp.com/api/swagger/) and [here](https://mess-management-server.herokuapp.com/api/redoc/).


Implemented Features 
=
1. Authentication
    * Users can register/login/logout from the app
    * Users can change the password
    * Users can update their payment modes to either pay-per-month service or buying coupons.

2. Bill
    * Users can get their bill details
    * Generate bills(caterer Side)
    * Razorpay integration for bill payments
    * Get a bill report

3. Complaint
    * Lodge a complaint
    * List all the complaints(caterer side)
    * Resolve complaints(caterer side)

4. Coupon
    * See the list of coupons
    * Every coupon has it's own unique UUID
    * Spend coupon by verifying scanning the generated QR Code(caterer side)
    * Buy coupons with Razorpay Integration

5. Leave
    * Request for leave
    * Leave approval(caterer side)

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
$ psql #verify if you can login to postgres without a password
$ \q #exit from psql
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
$ python3 manage.py createsuperuser
```
## Run Tests
```
$ python3 manage.py test
```
## Run Server
```
$ python3 manage.py runserver
```
> Enter your browser http://localhost:8000/. You can login via admin in http://localhost:8000/admin/.

Documentation
=
Visit http://localhost:8000/swagger/ for swagger endpoint or http://localhost:8000/redoc/ for redoc endpoint.

