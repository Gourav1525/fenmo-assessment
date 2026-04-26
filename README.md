# Expense Tracker

A minimal full-stack personal expense tracking application built with FastAPI and Streamlit.

## Live Demo
> Link will be added after deployment

## Features
- Add expenses with amount, category, description, and date
- View all expenses sorted by date (newest first)
- Filter expenses by category
- See total amount for the currently visible expenses
- Summary breakdown of spending per category
- Handles duplicate submissions gracefully (idempotency)
- Handles network errors and slow responses

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Database | SQLite |
| Language | Python 3.10 |

## Project Structure

```
fenmo-assessment/
├── backend/
│   ├── main.py         # FastAPI routes
│   ├── models.py       # Pydantic data models
│   └── database.py     # SQLite setup
├── frontend/
│   └── app.py          # Streamlit UI
├── requirements.txt
└── README.md
```

## Running Locally

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/fenmo-assessment.git
cd fenmo-assessment
```

**2. Create and activate virtual environment**
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Start the backend** (Terminal 1)
```bash
cd backend
uvicorn main:app --reload
```

**5. Start the frontend** (Terminal 2)
```bash
cd frontend
streamlit run app.py
```

**6. Open in browser**
```
http://localhost:8501
```

## API Endpoints

### POST /expenses
Create a new expense.
```json
{
  "amount": 150.00,
  "category": "Food",
  "description": "Lunch at café",
  "date": "2026-04-26",
  "idempotency_key": "unique-key-here"
}
```

### GET /expenses
Get all expenses with optional filters.
```
GET /expenses
GET /expenses?category=Food
GET /expenses?sort=date_desc
GET /expenses?category=Food&sort=date_desc
```

### GET /health
Health check endpoint.

## Key Design Decisions

**Money stored as integer (paise)**
Amount is stored as an integer in paise (1 rupee = 100 paise) to avoid floating point precision issues that are common with money in software. It is converted back to rupees only when returning responses.

**SQLite for persistence**
SQLite was chosen because it requires zero setup, is file-based, and is reliable for a single-user personal finance tool. It persists data across server restarts unlike an in-memory store. For a multi-user production system, PostgreSQL would be the right choice.

**Idempotency for safe retries**
Each form submission sends a unique idempotency key. If the same request is retried (due to network issues or double-clicking submit), the API detects the duplicate and returns the existing record instead of creating a new one. The key rotates after each successful submission.

**CORS enabled**
The backend allows all origins so the Streamlit frontend can communicate with the FastAPI backend without browser security blocks.

## Trade-offs Made

- No authentication — this is a personal tool, auth was out of scope for the timebox
- No pagination — kept simple since this is a personal tracker with limited data
- Streamlit for frontend — faster to build than a React app, acceptable for this scope
- SQLite instead of PostgreSQL — sufficient for single user, no infra setup needed

## Intentionally Not Done

- User authentication and multi-user support
- Pagination for large datasets
- Editing or deleting existing expenses
- Export to CSV or PDF
- Charts and visualizations beyond the category summary