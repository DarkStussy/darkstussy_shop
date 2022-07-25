# DESCRIPTION

This is my online shop. Implemented product categories, shopping cart, payment by card, invoice, output to PDF format. 
Convenient, adaptive interface. 

Stack: Bootstrap, Django, PostgreSQL, braintree.

# How to use the project:

!Requires PostgreSQL to run!

### CONSOLE

Cloning the project

> git clone https://github.com/DarkStussy/darkstussy_shop.git

> cd django_website

Create virtual environment

> python -m virtualenv venv

Activate virtual environment

WINDOWS:

> venv\Scripts\activate

LINUX:

> source venv\bin\activate

Installing the required dependencies

> pip install -r requirements.txt

Create database in psql and name db_shop.

Create an .env file in the root of the project and paste:

SECRET_KEY=<some secret_key>
BD_PASSWORD=<password postgresql>
BRAINTREE_MERCHANT_ID=<breaintree id>
BRAINTREE_PUBLIC_KEY=<public key>
BRAINTREE_PRIVATE_KEY=<private key>

Making database migrations

> python manage.py makemigrations

> python manage.py migrate

Run django server:

> python manage.py runserver

Ready!

To create a superuser, you need to enter the command:

> python manage.py createsuperuser
