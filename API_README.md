# MK8DX Table Reader - Web API

A FastAPI-based web API for extracting player names and scores from Mario Kart 8 Deluxe game screenshots.

## Features

- 🚀 **REST API** - Simple HTTP endpoints for image processing
- 📸 **Single Image Processing** - Upload one screenshot at a time
- 📚 **Batch Processing** - Process multiple images in one request
- 🔄 **CORS Enabled** - Ready for web browser requests
- 📊 **JSON Responses** - Easy to integrate with any application

## Installation

This will install all dependencies including the API requirements.

### Install from requirements.txt

```bash
pip install -r requirements.txt
```

## Running the API Server

### Quick Start

```bash
python api_server.py
```

The server will start on `http://localhost:8000`

### Using Uvicorn directly

```bash
uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload
```

Options:
- `--host 0.0.0.0` - Makes the server accessible from other machines
- `--port 8000` - Port to run on (change as needed)
- `--reload` - Auto-reload on code changes (development only)

## API Endpoints

### 1. Health Check

**GET** `/`

Check if the API is running.

```bash
curl http://localhost:8000/
```

Response:
```json
{
  "status": "online",
  "message": "MK8DX Table Reader API is running",
  "version": "1.0.0"
}
```

### 2. Detailed Health Check

**GET** `/health`

Check server health and model status.

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "models_loaded": true
}
```

### 3. Process Single Image

**POST** `/api/v1/read-table`

Upload an image and extract player data.

**Parameters:**
- `file` (required) - Image file (PNG, JPG, JPEG)

**Example using cURL:**

```bash
curl -X POST "http://localhost:8000/api/v1/read-table" \
  -F "file=@test_img.png" \
```

**Example using Python requests:**

```python
import requests

url = "http://localhost:8000/api/v1/read-table"
files = {"file": open("test_img.png", "rb")}

response = requests.post(url, files=files)
print(response.json())
```

**Response:**

```json
{
  "success": true,
  "table_detected": true,
  "team_mode": "FFA",
  "player_count": 12,
  "players": [
    {
      "position": 1,
      "name": "Player1",
      "score": "45"
    },
    {
      "position": 2,
      "name": "Player2",
      "score": "38"
    }
    // ... more players
  ]
}
```

## Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide a web interface to test the API endpoints directly in your browser.

## Error Responses

### 400 Bad Request
```json
{
  "detail": "File must be an image (PNG, JPG, JPEG)"
}
```

### 422 Unprocessable Entity
```json
{
  "detail": "No table detected in the image. Please ensure the image contains a valid MK8DX results table."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error processing image: [error details]"
}
```

## Testing the API

### Using the test images

You have test images in your repository. Try them:

```bash
curl -X POST "http://localhost:8000/api/v1/read-table" \
  -F "file=@test_img.png"
```

### Python test script

Run `test_api.py`:
```bash
python test_api.py
```

## Production Deployment

For production deployment, consider:

1. **Remove `reload=True`** from uvicorn configuration
2. **Use a production server** like Gunicorn with Uvicorn workers:
   ```bash
   pip install gunicorn
   gunicorn api_server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```
3. **Configure CORS** properly - update `allow_origins` to specific domains
4. **Add authentication** if needed
5. **Use HTTPS** with a reverse proxy (nginx, Apache)
6. **Add rate limiting** to prevent abuse
7. **Monitor and log** errors properly

## Troubleshooting

### CUDA/GPU issues
- The code attempts to use GPU if available
- If you have issues, edit `fullreader.py` to use CPU:
  ```python
  self.readerEasyOcr = easyocr.Reader(['en'], gpu=False)
  ```

## Support

For issues or questions, please open an issue on the GitHub repository.
