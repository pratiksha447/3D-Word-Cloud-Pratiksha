

---

# Running the Project Locally

This project includes a single setup script that installs all dependencies for both the backend (FastAPI) and frontend (React + Vite + React Three Fiber), then starts both servers.

Follow the steps below to run the application on your local machine.

---
## Prerequisites

Make sure your system has:

- macOS  
- Python 3.9+  
- Node.js 18+  
- npm (comes with Node)

---

## 1. Clone the repository

```bash
git clone https://github.com/<your-username>/3D-Word-Cloud-Pratiksha.git
cd 3D-Word-Cloud-Pratiksha
```

---

## 2. Run the setup script

From the project root:

```bash
./setup.sh
```

The script will:

1. Create a Python virtual environment in `backend/.venv`
2. Install backend dependencies (`FastAPI`, `uvicorn`, `BeautifulSoup`, `scikit-learn`, etc.)
3. Start the FastAPI backend at:

```
http://localhost:8000
```

4. Install frontend dependencies (`React`, `Vite`, `Three.js`, `React Three Fiber`, etc.)
5. Start the frontend development server at:

```
http://localhost:5173
```

Both servers will run concurrently.

---

## 3. Viewing the Application

Once the setup script finishes:

1. Open your browser  
2. Navigate to:

```
http://localhost:5173
```

You will see:

- A text input field for entering a news article URL  
- A button labeled **Analyze**  
- A 3D canvas area where the word cloud will appear  

---

## 4. How to Use the App

1. Enter any valid news article URL  
   (The UI includes a few sample URLs you can click or paste.)
2. Click **Analyze**
3. The frontend sends a POST request to:

```
POST http://localhost:8000/analyze
```

4. The backend:
   - Fetches the article HTML
   - Extracts readable text
   - Runs TF‑IDF keyword extraction
   - Returns a list of `{ word, weight }` items

5. The frontend renders the results as an interactive 3D word cloud using React Three Fiber.

You can rotate, zoom, and explore the word cloud with your mouse.

---

## 5. Troubleshooting

### Backend not responding
Check:

```
http://localhost:8000/health
```

You should see:

```json
{"status": "ok"}
```

If not, restart the backend:

```bash
cd backend
source .venv/bin/activate
uvicorn app:app --reload --port 8000
```

### Frontend shows “Failed to fetch”
This usually means CORS was not enabled. Ensure your `app.py` includes:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```