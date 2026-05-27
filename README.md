# Practice API — Documentation

Expense Tracker API built with **FastAPI**, plus separate scripts that practice HTTP calls with the `requests` library (external demo API and local API).

---

## Project structure

| File | Purpose |
|------|---------|
| `main.py` | FastAPI Expense Tracker server (local) |
| `get_all_objects.py` | GET all objects from external demo API |
| `get_single_object.py` | GET expenses from your local API |
| `post_an_object.py` | POST a new object to external demo API |
| `put_an_object.py` | PUT (update) an object on external demo API |
| `delete_object.py` | DELETE an object on external demo API |

---

## Setup (one time)

Open PowerShell in the project folder:

```powershell
cd "C:\Users\vidya.g\Documents\GitHub\practice_api"
```

Install dependencies:

```powershell
py -m pip install fastapi uvicorn requests pydantic
```

---

## `main.py` — Expense Tracker API

### Overview

- **Framework:** FastAPI
- **Server:** Uvicorn
- **Storage:** In-memory Python list (`expenses = []`)
- **App variable:** `vidya_expenses_app`
- **Port:** `8000`
- **Bind host:** `0.0.0.0` (listen on all interfaces; use `127.0.0.1` or `localhost` in the browser)

### Data model

```python
class Expense(BaseModel):
    title: str
    amount: float
    category: str
```

Each expense is stored as a dictionary, for example:

```json
{"title": "KFC", "amount": 600.5, "category": "Food"}
```

### API endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | Health check — API is running |
| GET | `/expenses` | List all expenses with count |
| POST | `/add-expense` | Add a new expense |
| GET | `/highest-expense` | Return the expense with the largest `amount` |

### Endpoint details

#### `GET /`

**Browser:** http://127.0.0.1:8000/

**Response example:**

```json
{"message": "Expense Tracker API Running"}
```

---

#### `GET /expenses`

**Browser:** http://127.0.0.1:8000/expenses

**PowerShell:**

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/expenses"
```

**Response example (after adding items):**

```json
{
  "count": 2,
  "expenses": [
    {"title": "KFC", "amount": 600.5, "category": "Food"},
    {"title": "Bus", "amount": 50.0, "category": "Travel"}
  ]
}
```

---

#### `POST /add-expense`

**Cannot use the browser address bar** (that sends GET only). Use Swagger, PowerShell, or a Python script.

**Swagger UI:** http://127.0.0.1:8000/docs → **POST /add-expense** → Try it out

**PowerShell:**

```powershell
$body = @{
  title    = "KFC"
  amount   = 600.5
  category = "Food"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/add-expense" -Method Post -Body $body -ContentType "application/json"
```

**curl (use `curl.exe` in PowerShell — `curl` alone is an alias for `Invoke-WebRequest`):**

```powershell
curl.exe -X POST "http://127.0.0.1:8000/add-expense" -H "Content-Type: application/json" -d "{\"title\":\"KFC\",\"amount\":600.5,\"category\":\"Food\"}"
```

**Response example:**

```json
{
  "message": "Expense added successfully",
  "expense": {"title": "KFC", "amount": 600.5, "category": "Food"}
}
```

**Behavior:** Each POST **appends** a new expense. It does **not** replace existing ones.

---

#### `GET /highest-expense`

**Browser:** http://127.0.0.1:8000/highest-expense

**PowerShell:**

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/highest-expense"
```

**Response when list is empty:**

```json
{"message": "No expenses found"}
```

**Response when expenses exist:**

```json
{"title": "KFC", "amount": 600.5, "category": "Food"}
```

Uses `max(expenses, key=lambda x: x["amount"])`.

---

### Run `main.py`

**Terminal 1 — start server (keep running):**

```powershell
cd "C:\Users\vidya.g\Documents\GitHub\practice_api"
python .\main.py
```

You should see:

```text
Uvicorn running on http://0.0.0.0:8000
```

**Open in browser (use `127.0.0.1`, not `0.0.0.0`):**

| Page | URL |
|------|-----|
| Root | http://127.0.0.1:8000/ |
| All expenses | http://127.0.0.1:8000/expenses |
| Highest expense | http://127.0.0.1:8000/highest-expense |
| Interactive API docs | http://127.0.0.1:8000/docs |

**Alternative start (without `if __name__` block):**

```powershell
uvicorn main:vidya_expenses_app --host 0.0.0.0 --port 8000
```

---

### Typical workflow (main.py)

1. Start server: `python .\main.py`
2. Add expenses (POST) in a **second** terminal
3. View list: browser → http://127.0.0.1:8000/expenses
4. View highest: browser → http://127.0.0.1:8000/highest-expense

**Example — add two expenses, then check highest:**

```powershell
# Expense 1
$body = @{ title="Bus"; amount=50; category="Travel" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/add-expense" -Method Post -Body $body -ContentType "application/json"

# Expense 2
$body = @{ title="KFC"; amount=600.5; category="Food" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/add-expense" -Method Post -Body $body -ContentType "application/json"

# List all
Invoke-RestMethod -Uri "http://127.0.0.1:8000/expenses"

# Highest
Invoke-RestMethod -Uri "http://127.0.0.1:8000/highest-expense"
```

---

### Important notes (main.py)

| Topic | Detail |
|-------|--------|
| In-memory storage | Restarting the server clears all expenses |
| `0.0.0.0` vs browser | Server binds to `0.0.0.0`; open `http://127.0.0.1:8000` in the browser |
| GET vs POST | Address bar = GET only. `/add-expense` requires POST |
| PowerShell `curl` | Use `curl.exe` or `Invoke-RestMethod` |
| PowerShell `GET` | Not a valid command; use `Invoke-RestMethod` |
| Empty `/highest-expense` | Add expenses first with POST `/add-expense` |

---

## Practice scripts (external API + local API)

These scripts use the **requests** library. They do **not** start a server (except you need `main.py` running for `get_single_object.py`).

**External demo API base URL:** `https://api.restful-api.dev/objects`

### `get_all_objects.py`

Fetches all objects from the external API and prints status, headers, text, and JSON.

```powershell
python .\get_all_objects.py
```

**No local server required.**

---

### `get_single_object.py`

Fetches expenses from **your local** Expense Tracker API.

**Requires:** `main.py` server running on port 8000.

```powershell
# Terminal 1
python .\main.py

# Terminal 2 (after adding at least one expense via POST)
python .\get_single_object.py
```

**Expected output shape:**

```json
{"count": 1, "expenses": [{"title": "KFC", "amount": 600.5, "category": "Food"}]}
```

---

### `post_an_object.py`

Creates a new object on the external API, then GETs all objects.

```powershell
python .\post_an_object.py
```

**No local server required.**

---

### `put_an_object.py`

Updates an existing object by ID on the external API.

**Note:** Replace the object ID in the `url` inside the file if the ID is no longer valid.

```powershell
python .\put_an_object.py
```

**No local server required.**

---

### `delete_object.py`

Deletes an object by ID on the external API.

**Note:** Replace the object ID in the `url` inside the file if needed.

```powershell
python .\delete_object.py
```

**No local server required.**

---

## Quick reference — all run commands

```powershell
cd "C:\Users\vidya.g\Documents\GitHub\practice_api"

# --- Expense Tracker (main.py) ---
python .\main.py

# In a second terminal (server must be running):
Invoke-RestMethod -Uri "http://127.0.0.1:8000/expenses"
Invoke-RestMethod -Uri "http://127.0.0.1:8000/highest-expense"

$body = @{ title="KFC"; amount=600.5; category="Food" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/add-expense" -Method Post -Body $body -ContentType "application/json"

# --- Practice scripts ---
python .\get_all_objects.py
python .\get_single_object.py      # needs main.py running
python .\post_an_object.py
python .\put_an_object.py
python .\delete_object.py
```

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|--------|-----|
| `NameError: uvicorn` | Missing import | Add `import uvicorn` at top of `main.py` |
| `ERR_ADDRESS_INVALID` for `0.0.0.0` | Browser cannot open bind address | Use http://127.0.0.1:8000 |
| `Method Not Allowed` on `/add-expense` | Browser sent GET | Use POST via `/docs` or PowerShell |
| `GET` not recognized in PowerShell | `GET` is not a cmdlet | Use `Invoke-RestMethod` |
| curl `-H` error in PowerShell | `curl` is `Invoke-WebRequest` alias | Use `curl.exe` or `Invoke-RestMethod` |
| `No expenses found` | Empty list or server restarted | POST expenses again, then open `/highest-expense` |
| `get_single_object.py` shows empty list | No expenses added to current server run | POST to `/add-expense`, then run script again |
| Long product list in terminal | Ran `get_all_objects.py` (external API) | Use `get_single_object.py` for local expenses |

---

## Architecture (simple)

```text
Browser / PowerShell / Python scripts
        |
        v
   FastAPI (main.py)  -->  expenses = []  (in RAM)
        |
        v
   Uvicorn :8000
```

External practice scripts talk directly to `https://api.restful-api.dev` (no FastAPI server).
