# Expense Tracker (Fenmo Assessment)

A minimal, production-aware full-stack expense tracking application built with Node.js and deployed on Vercel.

---

## Live Demo

👉 https://your-vercel-app.vercel.app
*(Replace with your actual deployed link — mandatory)*

---

## Features

* Add expenses (amount, category, description, date)
* View expenses sorted by newest first
* Filter by category
* Real-time total calculation for visible data
* Category-wise spending summary
* Idempotent API (prevents duplicate submissions)
* Handles network retries and failures gracefully

---

## Deployment

### Backend & Frontend (Vercel)

1. Set up a PostgreSQL database (e.g., on Supabase, Neon, or Vercel Postgres).
2. Set the `DATABASE_URL` environment variable in Vercel.
3. Deploy to Vercel: The entire project deploys as a static site with serverless API functions.

API endpoints will be available at `https://your-app.vercel.app/api/expenses`, etc.
Frontend will be served from the root URL.

For local development:
- Install dependencies: `npm install`
- Run development server: `npm run dev`
- Open `http://localhost:3000` in your browser

| Layer    | Technology        |
| -------- | ----------------- |
| Backend  | Express.js        |
| Frontend | Vanilla HTML/JS   |
| Database | PostgreSQL        |
| Runtime  | Node.js           |

---

## Project Structure

```
fenmo-assessment/
├── api/
│   ├── index.py
│   ├── models.py
│   └── database.py
├── frontend/
│   └── app.py
├── requirements.txt
├── vercel.json
├── .env.example
└── README.md
```

---

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/Gourav1525/fenmo-assessment.git
cd fenmo-assessment
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Setup environment variables

Create a `.env` file in the root directory:

```
DATABASE_URL=postgresql://username:password@localhost:5432/expenses_db
```

Replace:

* username → your PostgreSQL username
* password → your PostgreSQL password
* localhost:5432 → your DB host/port
* expenses_db → your database name

---

### 5. Start backend

```bash
cd backend
uvicorn main:app --reload
```

### 6. Start frontend

```bash
cd frontend
streamlit run app.py
```

### 7. Open app

```
http://localhost:8501
```

---

## API Endpoints

### POST /expenses

Create a new expense

```json
{
  "amount": 150.00,
  "category": "Food",
  "description": "Lunch",
  "date": "2026-04-26",
  "idempotency_key": "unique-key"
}
```

---

### GET /expenses

```
/expenses
/expenses?category=Food
/expenses?sort=date_desc
```

---

### GET /health

Health check endpoint

---

## Key Design Decisions

### Integer-based money handling

All monetary values are stored as integers (paise) to eliminate floating-point precision issues.

---

### PostgreSQL for persistence

Used PostgreSQL for reliable, production-ready storage with support for concurrent access and scalability.

---

### Idempotent API design

Each request includes an idempotency key to prevent duplicate expense entries during retries or accidental resubmissions.

---

### Separation of concerns

Clear distinction between frontend (Streamlit) and backend (FastAPI) for maintainability and scalability.

---

## Trade-offs

* No authentication (out of scope for time constraint)
* No pagination (optimized for personal use scale)
* Streamlit used for rapid UI development over React
* Limited feature set to prioritize stability and correctness

---

## Intentionally Not Implemented

* User authentication / multi-user support
* Edit/Delete functionality
* Export (CSV/PDF)
* Advanced analytics / charts

---

## Why This Stands Out

* Implements idempotency (rare in basic CRUD projects)
* Uses precision-safe money handling (integer storage)
* Production-aware backend design under strict time constraint
* Clean architecture with clear separation of layers
* Focus on reliability over feature bloat

---

## Environment Variables

The application uses environment variables for secure configuration.

### `.env` (DO NOT COMMIT)

```
DATABASE_URL=postgresql://username:password@localhost:5432/expenses_db
```

---

### `.env.example` (COMMITTED)

```
DATABASE_URL=postgresql://username:password@localhost:5432/expenses_db
```

---

### Important Notes

* `.env` must be added to `.gitignore`
* Never commit real database credentials
* For deployment (Render / Streamlit Cloud), set `DATABASE_URL` in the platform dashboard

---

## Author

Gourav Chouhan

---
