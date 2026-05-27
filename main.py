from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

vidya_expenses_app = FastAPI()

expenses = []
next_expense_id = 1


class Expense(BaseModel):
    title: str
    amount: float
    category: str


def ensure_expense_ids() -> None:
    """Assign ids to expenses added before id support (in-memory only)."""
    global next_expense_id
    for expense in expenses:
        if "id" not in expense:
            expense["id"] = next_expense_id
            next_expense_id += 1
    if expenses:
        next_expense_id = max(expense["id"] for expense in expenses) + 1


def find_expense_index(expense_id: int) -> Optional[int]:
    for index, expense in enumerate(expenses):
        if expense["id"] == expense_id:
            return index
    return None


@vidya_expenses_app.get("/")
def read_root():
    return {"message": "Expense Tracker API Running"}


@vidya_expenses_app.get("/expenses")
def get_expenses():
    ensure_expense_ids()
    return {
        "count": len(expenses),
        "expenses": expenses,
    }


@vidya_expenses_app.get("/expenses/{expense_id}")
def get_expense_by_id(expense_id: int):
    index = find_expense_index(expense_id)
    if index is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    return expenses[index]


@vidya_expenses_app.post("/add-expense")
def add_expense(expense: Expense):
    global next_expense_id

    expense_data = expense.model_dump()
    expense_data["id"] = next_expense_id
    next_expense_id += 1

    expenses.append(expense_data)

    return {
        "message": "Expense added successfully",
        "expense": expense_data,
    }


@vidya_expenses_app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, expense: Expense):
    index = find_expense_index(expense_id)
    if index is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    updated_expense = expense.model_dump()
    updated_expense["id"] = expense_id
    expenses[index] = updated_expense

    return {
        "message": "Expense updated successfully",
        "expense": updated_expense,
    }


@vidya_expenses_app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    index = find_expense_index(expense_id)
    if index is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    removed_expense = expenses.pop(index)

    return {
        "message": "Expense deleted successfully",
        "expense": removed_expense,
    }


@vidya_expenses_app.get("/highest-expense")
def highest_expense():
    if not expenses:
        return {"message": "No expenses found"}

    highest = max(expenses, key=lambda x: x["amount"])

    return highest


if __name__ == "__main__":
    uvicorn.run(vidya_expenses_app, host="0.0.0.0", port=8000)
