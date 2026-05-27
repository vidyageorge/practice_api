import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

vidya_expenses_app = FastAPI()

expenses = []


class Expense(BaseModel):
    title: str
    amount: float
    category: str


@vidya_expenses_app.get("/")
def read_root():
    return {"message": "Expense Tracker API Running"}


@vidya_expenses_app.get("/expenses")
def get_expenses():
    return {
        "count": len(expenses),
        "expenses": expenses,
    }


@vidya_expenses_app.post("/add-expense")
def add_expense(expense: Expense):
    expenses.append(expense.model_dump())

    return {
        "message": "Expense added successfully",
        "expense": expense,
    }

@vidya_expenses_app.get("/expenses")
def get_expenses():
   return expenses

if __name__ == "__main__":
    uvicorn.run(vidya_expenses_app, host="0.0.0.0", port=8000)
