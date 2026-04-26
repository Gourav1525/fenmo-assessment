from pydantic import BaseModel, field_validator
from typing import Optional
from decimal import Decimal


class ExpenseCreate(BaseModel):
    amount: Decimal
    category: str
    description: str
    date: str
    idempotency_key: Optional[str] = None

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Amount must be greater than zero")
        return v

    @field_validator("category")
    @classmethod
    def category_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Category cannot be empty")
        return v.strip()

    @field_validator("description")
    @classmethod
    def description_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Description cannot be empty")
        return v.strip()

    @field_validator("date")
    @classmethod
    def date_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Date cannot be empty")
        return v.strip()


class ExpenseResponse(BaseModel):
    id: str
    amount: float
    category: str
    description: str
    date: str
    created_at: str