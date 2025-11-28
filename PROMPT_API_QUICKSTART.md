# Prompt Management API - Quick Start Guide

This guide will help you get started with the Prompt Management API.

## Prerequisites

1. PostgreSQL database running (configured in `.env`)
2. Python dependencies installed
3. FastAPI server running

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Ensure your `.env` file contains:
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/postgres
   APP_NAME=Video_Risk_Assessment
   REGION=us-central1
   ```

3. **Initialize the database with seed data (optional):**
   ```bash
   python scripts/seed_prompts.py
   ```

## Running the Server

Start the FastAPI server using uvicorn:

```bash
uvicorn main:rest_api_app --reload --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`

## Testing the API

### Option 1: Interactive API Documentation

Open your browser and navigate to:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

These provide interactive documentation where you can test all endpoints directly.

### Option 2: Use the Test Script

Run the automated test script:

```bash
python scripts/test_prompt_api.py
```

This will execute all CRUD operations and display the results.

### Option 3: Manual Testing with cURL

**Create a prompt:**
```bash
curl -X POST "http://localhost:8000/prompts" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my_test_prompt",
    "content": "This is my test prompt content"
  }'
```

**Get all prompts:**
```bash
curl -X GET "http://localhost:8000/prompts"
```

**Get a specific prompt:**
```bash
curl -X GET "http://localhost:8000/prompts/1"
```

**Update a prompt:**
```bash
curl -X PUT "http://localhost:8000/prompts/1" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Updated prompt content"
  }'
```

**Delete a prompt:**
```bash
curl -X DELETE "http://localhost:8000/prompts/1"
```

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/prompts` | Create a new prompt |
| GET | `/prompts` | Get all prompts (with optional filters) |
| GET | `/prompts/{id}` | Get a specific prompt by ID |
| PUT | `/prompts/{id}` | Update a prompt's content |
| DELETE | `/prompts/{id}` | Delete a prompt |

## Common Use Cases

### 1. Creating a Prompt with Custom App Name and Region

```bash
curl -X POST "http://localhost:8000/prompts" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "custom_prompt",
    "content": "Custom prompt content",
    "app_name": "My_Custom_App",
    "region": "eu-west1"
  }'
```

### 2. Filtering Prompts by Application

```bash
curl -X GET "http://localhost:8000/prompts?app_name=Video_Risk_Assessment"
```

### 3. Filtering Prompts by Region

```bash
curl -X GET "http://localhost:8000/prompts?region=us-central1"
```

### 4. Filtering by Both App Name and Region

```bash
curl -X GET "http://localhost:8000/prompts?app_name=Video_Risk_Assessment&region=us-central1"
```

## Troubleshooting

### Database Connection Issues

If you encounter database connection errors:

1. Ensure PostgreSQL is running:
   ```bash
   # Check if PostgreSQL is running
   pg_isready
   ```

2. Verify database credentials in `.env`

3. Test database connection:
   ```bash
   psql postgresql://postgres:postgres@localhost:5432/postgres
   ```

### Port Already in Use

If port 8000 is already in use, start the server on a different port:

```bash
uvicorn main:rest_api_app --reload --port 8001
```

### Import Errors

If you encounter import errors, make sure all dependencies are installed:

```bash
pip install -r requirements.txt --upgrade
```

## Next Steps

- Refer to [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for detailed API documentation
- Check out the existing prompt service at `utils/prompt_service.py`
- Review the database models at `utils/models.py`

## Support

For issues or questions, please check:
1. Server logs for detailed error messages
2. FastAPI automatic documentation at `/docs`
3. Database connectivity and permissions
