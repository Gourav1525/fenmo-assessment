from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uuid
from datetime import datetime, timezone
from decimal import Decimal

from database import init_db, get_connection
from models import ExpenseCreate, ExpenseResponse

app = FastAPI(title="Expense Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()


@app.post("/expenses", response_model=ExpenseResponse, status_code=201)
def create_expense(expense: ExpenseCreate):
    conn = get_connection()
    cursor = conn.cursor()

    # Idempotency check — prevent duplicate submissions
    if expense.idempotency_key:
        cursor.execute(
            "SELECT * FROM expenses WHERE idempotency_key = ?",
            (expense.idempotency_key,)
        )
        existing = cursor.fetchone()
        if existing:
            conn.close()
            return ExpenseResponse(
                id=existing["id"],
                amount=existing["amount"] / 100,
                category=existing["category"],
                description=existing["description"],
                date=existing["date"],
                created_at=existing["created_at"],
            )

    # Store amount in paise (integer) to avoid float precision issues
    amount_in_paise = int(expense.amount * 100)
    expense_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    try:
        cursor.execute(
            """
            INSERT INTO expenses (id, amount, category, description, date, created_at, idempotency_key)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                expense_id,
                amount_in_paise,
                expense.category,
                expense.description,
                expense.date,
                created_at,
                expense.idempotency_key,
            ),
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

    return ExpenseResponse(
        id=expense_id,
        amount=float(expense.amount),
        category=expense.category,
        description=expense.description,
        date=expense.date,
        created_at=created_at,
    )


@app.get("/expenses", response_model=list[ExpenseResponse])
def get_expenses(
    category: Optional[str] = Query(None),
    sort: Optional[str] = Query(None),
):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM expenses WHERE 1=1"
    params = []

    if category:
        query += " AND LOWER(category) = LOWER(?)"
        params.append(category)

    if sort == "date_desc":
        query += " ORDER BY date DESC, created_at DESC"
    else:
        query += " ORDER BY date DESC, created_at DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [
        ExpenseResponse(
            id=row["id"],
            amount=row["amount"] / 100,
            category=row["category"],
            description=row["description"],
            date=row["date"],
            created_at=row["created_at"],
        )
        for row in rows
    ]


@app.get("/health")
def health():
    return {"status": "ok"}