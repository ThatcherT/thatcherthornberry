# Spotifly
Giving Spotify Wings.
## Getting Started
1. `pip install -r requirements.txt` Install Requirements
2. `python manage.py migrate` Create Database and Do Migrations
3. `python manage.py runserver` Run Server
## How it works
Users can text a certain phone number to create an account, follow their friends, and queue songs. By texting, their message is sent from the Twilio API to our Django API, then to the spotify API to do the actual queueing.
## Components
### Web Framework
Python Web Framework with Django
REST API with Django REST Framework
### Web Server
Gunicorn Web server running at https://spotifly.thatcherthornberry.com/
### Database
Postgresql Relational Database
