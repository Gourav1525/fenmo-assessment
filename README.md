# Expense Tracker (Fenmo Assessment)

A minimal full-stack expense tracker built with Node.js, Express, and PostgreSQL, deployed on Vercel.

---

## Live Demo

`https://your-app.vercel.app`

---

## Features

* Add expenses (amount, category, description, date)
* View expenses sorted by newest first
* Filter by category
* Total visible spending calculation
* Category summary breakdown
* Idempotent API to prevent duplicate submissions
* PostgreSQL persistence using Neon

---

## Deployment

### Vercel

1. Set the `DATABASE_URL` environment variable in your Vercel project.
2. Import the repository to Vercel.
3. Deploy the project.

The API will be available at `https://your-app.vercel.app/api/expenses` and the frontend will be served from the root URL.

---

## Local Development

### 1. Install Node.js

Download and install Node.js from https://nodejs.org.

### 2. Install dependencies

```bash
npm install
```

### 3. Run the app locally

```bash
npm run dev
```

### 4. Open in browser

```text
http://localhost:3000
```

---

## Environment

Create a `.env` file in the project root with:

```env
DATABASE_URL=postgresql://username:password@host:port/database?sslmode=require
```

---

## Project Structure

```
fenmo-assessment/
├── api/
│   ├── index.js
│   ├── database.js
│   └── models.js
├── index.html
├── package.json
├── vercel.json
├── .env
└── README.md
```

---

## API Endpoints

### POST /api/expenses

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

### GET /api/expenses

Query examples:

```
/api/expenses
/api/expenses?category=Food
/api/expenses?sort=date_desc
```

### GET /api/health

Health check endpoint

---

## Notes

- `.env` is ignored in git.
- On Vercel, static frontend files are served from the project root and API routes are handled under `/api`.


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
