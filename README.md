# Django + PostGIS API for managing geo points
API to create and manage places info with geo coordinates points.

## Features

- works in connection with PostgreSQL PostGIS extended.
- Django CRUD API - endpoints for listing, creating, editing and deleting places.
- create and update your profile, including profile picture, bio, and other details
- returns data in form of JSON response.
- create new posts with text content and optional media attachments 
- returns closes point to coordinates provided in form of request query for list endpoint
- documented with Swagger.
- docker compose file for easy deploy.

## Setting up project and getting started

Install using GitHUB
```sh
git clone https://github.com/amber-marichi/django-gis-api.git
cd django-gis-api
```

Set up variables
Prepare the .env file using .env.sample provided in project main directory. Change following values accordingly to database name, user name and password. Save file with variables as ".env"
```sh
DJANGO_SECRET_KEY=DJANGO_SECRET_KEY
DJANGO_DEBUG=0
POSTGRES_DB=POSTGRES_DB
POSTGRES_USER=POSTGRES_USER
POSTGRES_PASSWORD=POSTGRES_PASSWORD
PG_HOST=PG_HOST
```
! For PG_HOST use "db" value if project is to deploy using "docker compose up" command, use "localhost" value if database running locally.

### To run using Docker
!! Docker with docker compose must be installed and ready

Run docker compose command and wait for containers to build and start
```sh
docker compose up
```
Verify the deployment by navigating to your server address in
your preferred browser.

```sh
127.0.0.1:8000
```

### To run locally
!! Python3.8+ with pip should be installed and ready.
PostgreSQL database should be running locally or in Docker with creds corresponding to ones stated in your .env file. 

To easily set up PostgreSQL with PostGIS extension in Docker container use command:
```sh
docker run --name postgis-db -p 5432:5432 --mount type=volume,target=/postgis-data --env-file ./.env -d postgis/postgis:15-3.3-alpine
```

0. To use GeoDjango some Geospatial libraries must be installed. Such as GDAL, PROJ and GEOS. Please reffer to your platform-specific instructions, for Devian/Ubuntu system for example executing next shell command should work fine.

```sh
sudo apt-get install binutils libproj-dev gdal-bin
```

1. Create and activate venv:
```sh
python -m venv venv
```

2. Activate environment:

On Mac and Linux:
```sh
source venv/bin/activate
```
On Windows
```sh
venv/Scripts/activate
```

3. Install requirements:

```sh
pip install -r requirements.txt
```

4. Apply migrations

```sh
python manage.py migrate
```

5. Start the app:

```sh
python manage.py runserver
```

## To get access to the app
1. To get list of existing places or create new -
```sh
http://127.0.0.1:8000/api/places/
```

2. To get closest existing place to provided coordinates -
```sh
http://127.0.0.1:8000/api/places?lat=48.8583701&lng=2.2944813
```

3. To update or delete existing place by id -
```sh
http://127.0.0.1:8000/api/places/<id>/
```

4. To check out endpoints and their documentation for details.
```sh
http://127.0.0.1:8000/api/doc/swagger/
```
