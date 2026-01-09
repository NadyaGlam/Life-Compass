# Life Compass API

**Life Compass** is a **FastAPI-based backend service** that generates a structured personal development profile using precise astronomical calculations of lunar nodes.

The project is designed as a **production-style REST API** and demonstrates skills required for the US market:
- backend service design
- FastAPI & Pydantic
- object-oriented business logic
- logging and error handling
- clean Python project structure

---

##  Project Purpose

The service accepts a date, time, and place of birth and calculates:

- ☋ **South Lunar Node** — habitual patterns and comfort zone
- ☊ **North Lunar Node** — growth direction and development vector
- sign axis and house axis of the lunar nodes
- a structured, explainable transition profile

All calculations are **deterministic**, transparent, and based on astronomical data — no randomness or simplified lookup tables.

---

##  API Capabilities

- REST API built with FastAPI
- Automatic Swagger documentation (`/docs`)
- Input validation using Pydantic models
- Business logic encapsulated in a dedicated service class (OOP)
- Request, error, and process logging
- Integration with external data sources (coordinates, time zones)

---

##  Project Structure

```
LifeCompass/
├─ app/
│  ├─ api/              # FastAPI routes
│  ├─ services/         # Astronomical calculations & business logic
│  ├─ schemas/          # Pydantic models
│  ├─ core.py           # Business logic service class
│  ├─ logger.py         # Logging configuration
│  ├─ config.py         # Application settings
│  └─ main.py           # FastAPI application
├─ data/                # Places and coordinates data
├─ logs/                # Service logs
├─ run.py               # Application entry point
├─ requirements.txt
├─ README.md
└─ .gitignore
```

> The project structure is functionally equivalent to the reference structure from the technical assignment  
> (`app.py`, `core.py`, `schemas.py`, `logger.py`, `config.py`, `utilities.py`),  
> organized as a Python package for better scalability.

---

##  Installation

1. Clone the repository
2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the environment:

**Windows**
```bash
.venv\Scripts\activate
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

---

##  Running the Server

```bash
python run.py
```

After startup, open:

- Swagger UI: http://127.0.0.1:8000/docs

---

##  API Endpoints

- **GET /** — service status
- **GET /health** — health check
- **POST /profile** — generate Life Compass profile
- **GET /profile/place?q=...** — resolve place (coordinates and timezone)

---

##  Request Examples

### POST /profile

```json
{
  "birth_date": "1983-11-18",
  "birth_time": "14:30",
  "birth_place": "Miami, USA"
}
```

### Example Response

```json
{
  "title": "Sagittarius South Node → Gemini North Node",
  "bridge": "From absolute truth → to dialogue",
  "sections": [...],
  "recommendations": [...],
  "motto": "Truth is born in dialogue"
}
```

---

### GET /profile/place

```
/profile/place?q=Minsk
```

Response:
```json
{
  "query": "Minsk",
  "lat": 53.9,
  "lon": 27.56,
  "timezone": "Europe/Minsk"
}
```

---

##  Logging

The service uses structured logging:

- console output
- file logging to `logs/service.log`
- log levels: `INFO`, `WARNING`, `ERROR`

The following events are logged:
- service startup
- incoming HTTP requests
- key calculation steps
- errors and exceptions

---

##  Health & Verification

- The server starts using `python run.py`
- All endpoints are available via Swagger
- Logs are written to both console and `logs/service.log`
