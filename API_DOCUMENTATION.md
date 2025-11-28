# Prompt Management API Documentation

This document describes the REST API endpoints for managing prompts in the database.

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Create a New Prompt
Creates a new prompt in the database.

**Endpoint:** `POST /prompts`

**Request Body:**
```json
{
  "name": "example_prompt",
  "content": "This is the prompt content",
  "app_name": "Video_Risk_Assessment",  // Optional, defaults to env variable
  "region": "us-central1"                // Optional, defaults to env variable
}
```

**Response:** (Status: 201 Created)
```json
{
  "id": 1,
  "name": "example_prompt",
  "app_name": "Video_Risk_Assessment",
  "region": "us-central1",
  "version": 1,
  "content": "This is the prompt content",
  "created_at": "2025-11-28 12:47:01.123456"
}
```

**Error Response:**
- `400 Bad Request` - If a prompt with the same name, app_name, and region already exists
- `500 Internal Server Error` - If there's a database error

**Example using cURL:**
```bash
curl -X POST "http://localhost:8000/prompts" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test_prompt",
    "content": "This is a test prompt content"
  }'
```

---

### 2. Get All Prompts
Retrieves all prompts, optionally filtered by app_name and/or region.

**Endpoint:** `GET /prompts`

**Query Parameters:**
- `app_name` (optional): Filter by application name
- `region` (optional): Filter by region

**Response:** (Status: 200 OK)
```json
[
  {
    "id": 1,
    "name": "example_prompt",
    "app_name": "Video_Risk_Assessment",
    "region": "us-central1",
    "version": 1,
    "content": "This is the prompt content",
    "created_at": "2025-11-28 12:47:01.123456"
  },
  {
    "id": 2,
    "name": "another_prompt",
    "app_name": "Video_Risk_Assessment",
    "region": "us-central1",
    "version": 2,
    "content": "Another prompt content",
    "created_at": "2025-11-28 12:48:01.123456"
  }
]
```

**Example using cURL:**
```bash
# Get all prompts
curl -X GET "http://localhost:8000/prompts"

# Get prompts filtered by app_name
curl -X GET "http://localhost:8000/prompts?app_name=Video_Risk_Assessment"

# Get prompts filtered by both app_name and region
curl -X GET "http://localhost:8000/prompts?app_name=Video_Risk_Assessment&region=us-central1"
```

---

### 3. Get Prompt by ID
Retrieves a specific prompt by its ID.

**Endpoint:** `GET /prompts/{prompt_id}`

**Path Parameters:**
- `prompt_id`: The ID of the prompt to retrieve

**Response:** (Status: 200 OK)
```json
{
  "id": 1,
  "name": "example_prompt",
  "app_name": "Video_Risk_Assessment",
  "region": "us-central1",
  "version": 1,
  "content": "This is the prompt content",
  "created_at": "2025-11-28 12:47:01.123456"
}
```

**Error Response:**
- `404 Not Found` - If the prompt with the specified ID doesn't exist
- `500 Internal Server Error` - If there's a database error

**Example using cURL:**
```bash
curl -X GET "http://localhost:8000/prompts/1"
```

---

### 4. Update Prompt
Updates an existing prompt's content and increments its version.

**Endpoint:** `PUT /prompts/{prompt_id}`

**Path Parameters:**
- `prompt_id`: The ID of the prompt to update

**Request Body:**
```json
{
  "content": "Updated prompt content"
}
```

**Response:** (Status: 200 OK)
```json
{
  "id": 1,
  "name": "example_prompt",
  "app_name": "Video_Risk_Assessment",
  "region": "us-central1",
  "version": 2,
  "content": "Updated prompt content",
  "created_at": "2025-11-28 12:47:01.123456"
}
```

**Error Response:**
- `404 Not Found` - If the prompt with the specified ID doesn't exist
- `500 Internal Server Error` - If there's a database error

**Example using cURL:**
```bash
curl -X PUT "http://localhost:8000/prompts/1" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Updated content for the prompt"
  }'
```

---

### 5. Delete Prompt
Deletes a prompt by its ID.

**Endpoint:** `DELETE /prompts/{prompt_id}`

**Path Parameters:**
- `prompt_id`: The ID of the prompt to delete

**Response:** (Status: 204 No Content)
No response body

**Error Response:**
- `404 Not Found` - If the prompt with the specified ID doesn't exist
- `500 Internal Server Error` - If there's a database error

**Example using cURL:**
```bash
curl -X DELETE "http://localhost:8000/prompts/1"
```

---

## Interactive API Documentation

FastAPI automatically generates interactive API documentation. Once your server is running, you can access:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

These interfaces allow you to test the API endpoints directly from your browser.

---

## Notes

1. **Version Management:** When you update a prompt using the PUT endpoint, the version is automatically incremented.

2. **Unique Constraint:** The combination of `name`, `app_name`, and `region` must be unique. You cannot create two prompts with the same combination.

3. **Default Values:** If you don't provide `app_name` or `region` when creating a prompt, they will default to the values from environment variables (`APP_NAME` and `REGION`), or to `"Video_Risk_Assessment"` and `"us-central1"` respectively.

4. **Database Initialization:** The database tables are automatically initialized when the application starts.

---

## Environment Variables

Make sure to set these in your `.env` file:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/postgres
APP_NAME=Video_Risk_Assessment
REGION=us-central1
```
