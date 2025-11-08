# Mobile Attendance System - FastAPI Backend

Production-ready FastAPI backend for mobile attendance tracking with Bluetooth integration.

## 📁 Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── database.py             # Database configuration and session management
├── models.py               # SQLAlchemy ORM models
├── schemas.py              # Pydantic validation schemas (versioned)
├── crud.py                 # Database CRUD operations
├── config.py               # Application configuration
├── routers/
│   ├── attendance_v1.py    # Version 1 API endpoints
│   └── attendance_v2.py    # Version 2 placeholder (future)
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
└── README.md              # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database

Copy `.env.example` to `.env` and update with your PostgreSQL credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/bluscan_db
```

### 3. Create Database

```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE bluscan_db;

# Exit
\q
```

### 4. Run the Application

```bash
# Development mode with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. Access API Documentation

- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 📡 API Endpoints

### Version 1 Endpoints (`/api/v1/`)

#### POST `/api/v1/attendance/`
Submit attendance record from Android app.

**Request:**
```json
{
  "student_id": "STU123",
  "device_mac": "AA:BB:CC:DD:EE:FF",
  "timestamp": "2025-11-08T10:30:00",
  "bluetooth_signal_strength": -45,
  "status": "present"
}
```

**Response:**
```json
{
  "message": "Attendance record stored successfully"
}
```

#### GET `/api/v1/attendance/`
Fetch all attendance records (for React frontend).

**Query Parameters:**
- `skip`: Pagination offset (default: 0)
- `limit`: Max records to return (default: 100)
- `student_id`: Filter by student ID (optional)

**Response:**
```json
{
  "total": 150,
  "records": [
    {
      "id": 1,
      "student_id": "STU123",
      "device_mac": "AA:BB:CC:DD:EE:FF",
      "timestamp": "2025-11-08T10:30:00",
      "bluetooth_signal_strength": -45,
      "status": "present",
      "created_at": "2025-11-08T10:30:05",
      "updated_at": null
    }
  ]
}
```

#### GET `/api/v1/attendance/{record_id}`
Fetch single attendance record by ID.

#### DELETE `/api/v1/attendance/{record_id}`
Delete attendance record by ID.

## 🔄 API Versioning

The system supports versioned APIs to handle future schema changes:

- **Current:** `/api/v1/attendance/` (active)
- **Future:** `/api/v2/attendance/` (placeholder ready)

### Adding a New Version

1. Update `schemas.py` with new Pydantic models
2. Create new router file (e.g., `routers/attendance_v3.py`)
3. Register router in `main.py`:
```python
app.include_router(attendance_v3.router, prefix="/api/v3", tags=["Attendance V3"])
```

## 🔐 Security Features

- CORS middleware configured for React and Android
- Pydantic validation prevents invalid data
- `extra='ignore'` handles unexpected JSON fields gracefully
- SQL injection protection via SQLAlchemy ORM
- Connection pooling for database performance

## 📝 Logging

All API calls are logged with:
- Received JSON data
- Response status
- Error details (if any)

Logs include:
- ✓ Success indicators
- ✗ Error indicators
- Timestamps and log levels

## 🧪 Testing

### Test POST endpoint (Android simulation)
```bash
curl -X POST "http://localhost:8000/api/v1/attendance/" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU123",
    "device_mac": "AA:BB:CC:DD:EE:FF",
    "timestamp": "2025-11-08T10:30:00",
    "bluetooth_signal_strength": -45,
    "status": "present"
  }'
```

### Test GET endpoint (React simulation)
```bash
curl -X GET "http://localhost:8000/api/v1/attendance/?limit=10"
```

## 🐳 Docker Deployment (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: bluscan_db
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://user:password@db:5432/bluscan_db
    depends_on:
      - db

volumes:
  postgres_data:
```

Run with Docker:
```bash
docker-compose up -d
```

## 🔧 Database Migrations (Alembic)

Initialize Alembic:
```bash
alembic init alembic
```

Create migration:
```bash
alembic revision --autogenerate -m "Create attendance table"
```

Apply migration:
```bash
alembic upgrade head
```

## 📱 Android Integration

Configure Android app to send POST requests:

```kotlin
// Retrofit example
interface AttendanceApi {
    @POST("api/v1/attendance/")
    suspend fun submitAttendance(
        @Body attendance: AttendanceData
    ): MessageResponse
}

data class AttendanceData(
    val student_id: String,
    val device_mac: String,
    val timestamp: String,
    val bluetooth_signal_strength: Float,
    val status: String
)
```

## ⚛️ React Integration

Fetch attendance records:

```javascript
// Fetch all records
const response = await fetch('http://localhost:8000/api/v1/attendance/');
const data = await response.json();

// Filter by student
const response = await fetch(
  'http://localhost:8000/api/v1/attendance/?student_id=STU123'
);
const data = await response.json();
```

## 🛠️ Production Checklist

- [ ] Change `SECRET_KEY` in `.env`
- [ ] Configure specific CORS origins
- [ ] Set up HTTPS/SSL
- [ ] Enable database backups
- [ ] Configure logging to file
- [ ] Set up monitoring (e.g., Sentry)
- [ ] Use environment variables for all secrets
- [ ] Set up reverse proxy (Nginx/Caddy)
- [ ] Configure rate limiting
- [ ] Enable database connection pooling

## 📄 License

This project is part of the Mobile Attendance System.