## Features

- JWT Authentication (Login & Refresh)

- Create, Read, Update, Delete Snippets

- Unique Tags (no duplicate tags)

- Many-to-Many relationship between Snippet and Tag

- Overview API (total count + listing)

- Tag-based snippet listing

- Swagger API documentation

- Docker support

- PEP-8 compliant code

## Tech Stack

- Python 3.10+

- Django 4.x

- Django Rest Framework

- djangorestframework-simplejwt

- drf-yasg (Swagger)

- SQLite (default database)

- Docker

## Installation (Without Docker)

1. Clone the repository

    - git clone [<github_repo_link>](https://github.com/Resho-techie/snipbox-backend)
    - cd snipbox

2. Create virtual environment
    
    - python -m venv venv
    - source venv/bin/activate

3. Install dependencies

    - pip install -r requirements.txt

4. Run migrations

    - python manage.py makemigrations
    - python manage.py migrate

5. Create superuser or load fixtures

    - python manage.py createsuperuser
    - python manage.py loaddata initial_data.yaml

6. Run the server

    - python manage.py runserver

7. Open Link at : http://127.0.0.1:8000/

###### APIs #####

# Login

POST /api/login/

Request Body:

{
  "username": "admin",
  "password": "yourpassword"
}

Returns access and refresh tokens.

# Refresh Token

POST /api/refresh/

{
  "refresh": "<refresh_token>"
}

# Snippet APIs

GET /api/snippets/overview/ → Total count + list

POST /api/snippets/ → Create snippet

GET /api/snippets/{id}/ → Get snippet detail (owner only)

PUT /api/snippets/{id}/ → Update snippet

DELETE /api/snippets/{id}/ → Delete snippet (returns updated list)

# Tag APIs

GET /api/tags/ → List all tags

GET /api/tags/{id}/ → Get snippets under selected tag

## Database Schema

Database schema diagram is available in:

docs/schema.png

Generated using:

python manage.py graph_models -a -o docs/schema.png

## Run with Docker

1. Build

    docker compose build

2. Run

    docker compose up

3. Application

    Open at http://localhost:8000/

**Note:*** docker compose exec web python manage.py loaddata initial_data.yaml

## Requirements

All dependencies are listed in requirements.txt.

pip install -r requirements.txt

**Note:** Find API doc in docs/api_test.md

## Sample Fixture Data

This project includes a sample fixture file (`initial_data.yaml`) 
for demonstration purposes only.
