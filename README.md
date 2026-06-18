# Voyago Chatbot - FastAPI Backend
<img width="800" height="533" alt="image" src="https://github.com/user-attachments/assets/0471c02d-eac7-490b-b45a-a515344db825" />

AI-powered tourism chatbot backend for Fayoum - Egypt. Built with **FastAPI**, **scikit-learn**, and **pandas**, supporting both **Arabic and English** with context memory, intent classification, and emergency detection.

---

##  Quick Start (Local Windows)

If you are on Windows, we have provided a shortcut to run the server instantly:
1. Double-click the file [run.bat](file:///c:/Users/GRAPHICS/Downloads/voyago-chatbot/voyago-chatbot/run.bat) located in the project root directory.
2. The server will start on `http://localhost:8000`.

---

## 🛠️ Tech Stack & Architecture

- **Framework**: FastAPI (Python)
- **NLP & Machine Learning**: `scikit-learn` & `pandas` (intent classification via TF-IDF + Logistic Regression/SVM)
- **Web Client**: `httpx` (async API client to connect to core backend)
- **Deployment**: Docker & Docker Compose
- **Design Pattern**: 3-Layer Architecture (API Layer -> Service/NLP Layer -> Data/Integration Layer)

---

## ⚙️ Environment Configuration

Create a `.env` file in the root directory (based on `.env.example`):

```env
# URL base of the core Voyago backend
VOYAGO_API_BASE=http://voyagoo.runasp.net

# API endpoints to fetch tourist data
HOTELS_ENDPOINT=/hotels
ATTRACTIONS_ENDPOINT=/Attractions
RESTAURANTS_ENDPOINT=/Restaurants
TOURGUIDES_ENDPOINT=/TourGuides

# CORS allowed origins (* for development)
ALLOWED_ORIGINS=["*"]

# Maximum context conversation turns to remember
CONTEXT_MAX_TURNS=5

# Path to the training dataset
DATASET_PATH=data/voyago_dataset.csv
```

---

## 💻 Manual Installation & Running

### 1. Prerequisites
- Python 3.10 or higher (compatible up to Python 3.13)

### 2. Create Virtual Environment & Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Server
```bash
python -m app.main
```
The server will start at `http://127.0.0.1:8000`.

### 4. Running the Tests
To verify all chatbot functions (Emergency, Language, Intent, Response builder):
```bash
python -m pytest tests/ -v
```

---

## 🐳 Docker Deployment

The project is fully containerized. You can run the entire application using Docker Compose:

```bash
# Start container in detached mode
docker compose up -d --build
```
This builds a multi-stage, lightweight image based on `python:3.11-slim` and starts the chatbot API on port `8000`.

---

##  API Endpoints Documentation

### 1. Interactive Swagger UI
Open your browser and navigate to:
* **`http://localhost:8000/docs`**

Here you can test all API endpoints directly from the browser.

---

### 2. Chat Endpoint (`POST /chat`)
Handles chatbot messages, intent mapping, Arabic/English NLP, database matching, and emergency response.

* **URL:** `/chat`
* **Method:** `POST`
* **Headers:** `Content-Type: application/json`
* **Request Body:**
```json
{
  "message": "عايز فندق في الفيوم",
  "session_id": "session_123",
  "language": "auto"
}
```

* **Response Body (Example):**
```json
{
  "message": " **Fayoum Hotels**\n\nHere are the best accommodation options in Fayoum...",
  "type": "card",
  "data": {
    "items": [
      {
        "id": 3,
        "name": "Lazib Inn Resort & Spa",
        "rating": 4.5,
        "image": null,
        "price": null,
        "link": "http://voyagoo.runasp.net/hotels/3"
      }
    ]
  },
  "intent": "fayoum_hotels",
  "language": "ar"
}
```

---

### 3. Health Check (`GET /health`)
Verifies server health and model state.

* **URL:** `/health`
* **Method:** `GET`
* **Response:**
```json
{
  "status": "ok",
  "model": "voyago-v1"
}
```
