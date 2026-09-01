# Campus Venue Reservation System

An institutional venue reservation and scheduling management platform engineered with a high-performance **FastAPI** backend and a responsive **Glassmorphism UI**. Designed to streamline campus auditorium and seminar hall bookings through automated schedule collision detection, instant SMTP email dispatch, and role-based administrative control.

---

## Key Features

* ** Collision Detection Engine**: Automatically audits requested time slots to prevent overlapping reservations and double-bookings.
* ** Automated SMTP Mail Service**: Dispatches HTML booking confirmations with reference IDs to faculty and alerts upon slot cancellation.
* ** JWT-Secured Admin Console**: Token-authenticated management panel with live ledger monitoring and venue slot cancellation controls.
* ** Dynamic Excel Ledger Export**: Generates and downloads the official `.xlsx` reservation ledger directly from database records.
* ** Frosted Glassmorphism UI**: Custom interface with institutional branding, NAAC A++ accreditation badges, and an intuitive 12-hour AM/PM date-time picker.
* ** Serverless Deployment Ready**: Structured for deployment on Vercel with dedicated API routing rewrites.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+) |
| **Data & ORM** | [SQLAlchemy](https://www.sqlalchemy.org/), SQLite / PostgreSQL |
| **Data Validation** | [Pydantic v2](https://docs.pydantic.dev/) & Pydantic-Settings |
| **Authentication** | OAuth2 with JWT Bearer Tokens (`python-jose`, `passlib`) |
| **Reports Engine** | [OpenPyXL](https://openpyxl.readthedocs.io/) |
| **Frontend** | HTML5, CSS3 Glassmorphism, Vanilla JavaScript |
| **Components** | [Flatpickr](https://flatpickr.js.org/) (Custom 12-Hour Range Picker) |
| **Hosting & Functions** | [Vercel](https://vercel.com/) Serverless Python Runtime |

---

##  Project Structure

```text
├── api/
│   └── index.py            # Vercel serverless entry point
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── admin.py    # Authenticated management & export endpoints
│   │   │   └── bookings.py # Public reservation & collision detection routes
│   │   ├── auth.py         # JWT generation & password hashing
│   │   ├── config.py       # Pydantic environment configuration
│   │   ├── database.py     # SQLAlchemy session setup
│   │   ├── email_service.py# SMTP dispatch engine
│   │   ├── main.py         # FastAPI root application instance
│   │   ├── models.py       # Relational database tables
│   │   └── schemas.py      # Request & response data models
│   └── .env                # Local secrets (excluded from Git)
├── frontend/
│   ├── index.html          # Public booking portal
│   ├── admin.html          # Admin dashboard & ledger
│   ├── college-logo.png    # Primary institutional logo
│   ├── college-bg.jpg      # Glassmorphic background
│   └── naac-logo.png       # Accreditation badge
├── requirements.txt        # Production dependencies
└── vercel.json             # Serverless routing rules
```

---

## 🚀 Quick Start (Local Setup)

### 1. Clone the Repository
```bash
git clone https://github.com/<YOUR_USERNAME>/<REPO_NAME>.git
cd <REPO_NAME>
```

### 2. Set Up Virtual Environment & Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file inside the `backend/` directory:

```env
SECRET_KEY=your_custom_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480
DATABASE_URL=sqlite:///./hall_booking.db

# SMTP Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=your_institution_mail@gmail.com
SMTP_PASSWORD=your_16_character_app_password
SENDER_NAME="Campus Venue Reservation"
```

### 4. Run the Application
```bash
# Start FastAPI backend server
cd backend
uvicorn app.main:app --reload --port 8080
```

* **Public Booking Portal:** Open `frontend/index.html` via Live Server or browser at `http://localhost:3000`
* **Admin Dashboard:** Open `frontend/admin.html`
* **Interactive API Documentation (Swagger):** Visit `http://127.0.0.1:8080/docs`

---

##  Deployment to Vercel

1. **Push to GitHub**: Push the repository code ensuring `.env` and `venv/` are excluded via `.gitignore`.
2. **Import to Vercel**: Connect your GitHub repository to Vercel.
3. **Configure Environment Variables**:
   Under **Project Settings** → **Environment Variables**, add:
   * `SECRET_KEY`
   * `ALGORITHM`
   * `ACCESS_TOKEN_EXPIRE_MINUTES`
   * `SMTP_HOST`
   * `SMTP_PORT`
   * `SMTP_USER`
   * `SMTP_PASSWORD`
   * `SENDER_NAME`
4. **Deploy**: Click **Deploy**. Vercel will build and serve the API via `api/index.py` and map the frontend according to `vercel.json`.
