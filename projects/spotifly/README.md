# Spotifly

Giving Spotify Wings.

## Getting Started

1. `pip install -r requirements.txt` Install Requirements
2. `python manage.py migrate` Create Database and Do Migrations
3. `python manage.py runserver` Run Server

## How it works

A progressive web app where users exist on a device basis using localstorage. Users can "follow" users who have authenticated with Spotify. After following, users can use the UI to queue songs to their device.

## Components

### Web Framework

Django

### Web Server

Gunicorn Web server running at https://qsongs.thatcherthornberry.com/

### Database

Postgresql Relational Database
