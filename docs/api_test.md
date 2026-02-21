## Access API Docs

# Swagger UI

http://localhost:8000/swagger/

# ReDoc UI:

http://localhost:8000/redoc/


Base URL:
http://127.0.0.1:8000/

## Login API

# Request

POST /api/login/

curl -X POST http://127.0.0.1:8000/api/login/ \
-H "Content-Type: application/json" \
-d '{
  "username": "admin",
  "password": "yourpassword"
}'

# Response
{
  "access": "access_token",
  "refresh": "refresh_token"
}

## Refresh Token API

POST /api/refresh/

curl -X POST http://127.0.0.1:8000/api/refresh/ \
-H "Content-Type: application/json" \
-d '{
  "refresh": "<refresh_token>"
}'

### Snippet APIs ###

## Overview API

GET /api/snippets/overview/

curl -X GET http://127.0.0.1:8000/api/snippets/overview/ \
-H "Authorization: Bearer <access_token>"

# Response
{
  "total_snippets": 2,
  "snippets": [
    {
      "id": 1,
      "title": "Django Note",
      "detail_url": "http://127.0.0.1:8000/api/snippets/1/"
    }
  ]
}

## Create Snippet API

POST /api/snippets/

curl -X POST http://127.0.0.1:8000/api/snippets/ \
-H "Authorization: Bearer <access_token>" \
-H "Content-Type: application/json" \
-d '{
  "title": "DRF Notes",
  "note": "Django Rest Framework is powerful",
  "tags": ["django", "backend"]
}'

## Detail API

GET /api/snippets/{id}/

curl -X GET http://127.0.0.1:8000/api/snippets/1/ \
-H "Authorization: Bearer <access_token>"

## Update API

PUT /api/snippets/{id}/

curl -X PUT http://127.0.0.1:8000/api/snippets/1/ \
-H "Authorization: Bearer <access_token>" \
-H "Content-Type: application/json" \
-d '{
  "title": "Updated Title",
  "note": "Updated note",
  "tags": ["updated", "django"]
}'

## Delete API

DELETE /api/snippets/{id}/

curl -X DELETE http://127.0.0.1:8000/api/snippets/1/ \
-H "Authorization: Bearer <access_token>"

## Tag List API

GET /api/tags/

curl -X GET http://127.0.0.1:8000/api/tags/ \
-H "Authorization: Bearer <access_token>"

## Tag Detail API

GET /api/tags/{id}/

curl -X GET http://127.0.0.1:8000/api/tags/1/ \
-H "Authorization: Bearer <access_token>"

## Note

- ll snippet operations are user-specific.

- Tags are unique.

- Existing tag titles are reused instead of creating duplicates.

- JWT authentication is required for all protected endpoints.