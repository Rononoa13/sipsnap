SipSnap 🍹

SipSnap is an AI-powered menu scanning application that turns a photo of a drinks menu into a structured digital menu.

The application uses a FastAPI backend for image processing and AI-powered menu extraction, with a lightweight JavaScript frontend served separately during development.

Architecture

                    ┌─────────────────────┐
                    │       Phone         │
                    │   Camera / Browser  │
                    └──────────┬──────────┘
                               │
                               │ HTTP
                               ▼
                    ┌─────────────────────┐
                    │      Frontend       │
                    │   Python HTTP       │
                    │     :8080           │
                    └──────────┬──────────┘
                               │
                               │ API requests
                               ▼
                    ┌─────────────────────┐
                    │       Backend       │
                    │   FastAPI/Uvicorn   │
                    │      :8000          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Gemini        │
                    │    Vision / AI      │
                    └─────────────────────┘

Services

Service	Directory	Server	Port
Backend	backend/	Uvicorn / FastAPI	8000
Frontend	frontend/	Python HTTP server	8080

⸻

Project Structure

sipsnap/
├── backend/
│   ├── ...
│   └── ...
│
├── frontend/
│   ├── scan.html
│   ├── results.html
│   ├── camera.js
│   └── ...
│
├── .env
├── .gitignore
└── README.md

⸻

Running Locally

SipSnap currently runs as two separate HTTP servers:

* FastAPI backend → localhost:8000
* Frontend → localhost:8080

You need to run both servers.

1. Start the Backend

From the project root:

uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

The backend will be available at:

http://localhost:8000

FastAPI’s interactive API documentation is available at:

http://localhost:8000/docs

⸻

2. Start the Frontend

Open another terminal and serve the frontend/ directory:

cd frontend
python3 -m http.server 8080

The frontend will be available at:

http://localhost:8080

Open:

http://localhost:8080/scan.html

⸻

Using SipSnap from a Phone

For testing the camera functionality on a phone, both the computer and phone need to be connected to the same local network.

Find your computer’s local IP address.

For example:

192.168.1.10

Then open the frontend from your phone:

http://192.168.1.10:8080/scan.html

The backend continues running on port 8000.

The important distinction is:

Phone
  │
  │ :8080
  ▼
Frontend
  │
  │ API request :8000
  ▼
Backend

When accessing SipSnap from another device, localhost refers to that device itself, so the frontend should use the computer’s LAN IP when making requests to the backend.

⸻

Environment Variables

Create a .env file for local configuration:

GEMINI_API_KEY=your_api_key_here

Do not commit .env to Git.

Make sure it is included in .gitignore:

.env

⸻

Development

Backend

The backend is built with:

* Python
* FastAPI
* Uvicorn
* Pydantic Settings

Start it with:

uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

Frontend

The frontend is intentionally lightweight and uses:

* HTML
* CSS
* Vanilla JavaScript
* Browser Camera APIs

Start it with:

cd frontend
python3 -m http.server 8080

⸻

API

The frontend communicates with the FastAPI backend over HTTP.

Example:

POST /...

The request contains the captured menu image.

The backend sends the image to the AI service for menu extraction and returns structured data to the frontend.

⸻

Current MVP Scope

SipSnap currently focuses on the core menu-scanning workflow:

1. Open the application.
2. Capture or select a menu photo.
3. Upload the image to the backend.
4. Process the menu using AI vision.
5. Extract drinks from the menu.
6. Display the extracted menu in the browser.

The MVP intentionally keeps the scope small and does not currently include:

* User accounts
* Payments
* Taste profiles
* Personalized recommendations
* Social features

⸻

Tech Stack

Frontend

HTML
CSS
Vanilla JavaScript
Web APIs

Backend

Python
FastAPI
Uvicorn
Pydantic

AI

Google Gemini

Development

Git
Docker
Python HTTP Server

⸻

Future Improvements

Potential future improvements include:

* Canonical drink-name inference
* Drink image lookup/generation
* Better menu extraction
* Improved mobile UI
* Production deployment
* HTTPS
* Persistent menu storage
* User accounts
* Personalized recommendations

⸻

License

This project is currently under development.