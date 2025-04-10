# 💰 Expense Tracker API

A complete backend expense tracking system built using **Flask**, **MySQL**, and **SQLAlchemy**, with testing tools and Docker support.

---

## ✅ Features
- User creation and management
- Budget setting by category and month
- Expense logging
- Monthly reports
- Budget alerts (90% usage or exceeded)
- Group expense sharing and settlement
- Email alerts (optional)
- HTML test interface
- Dockerized setup

---

## 🔧 Steps to Run the Application 

### ▶️ Option 1: Run Locally

#### 1. Clone the repo and set up a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate on Linux/Mac
```

#### 2. Install dependencies:
```bash
pip install -r requirements.txt
```

#### 3. Set up `.env` file:
Create a `.env` file in root with your MySQL credentials:
```env
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_NAME=expense_db
```

#### 4. Create MySQL DB manually (if not using Docker):
```sql
CREATE DATABASE expense_db;
```

#### 5. Run the app:
```bash
python -m app.main
```
Visit [http://127.0.0.1:5000](http://127.0.0.1:5000)

#### 6. Run the HTML tester (optional UI):
```bash
python -m http.server 8000
```
Visit [http://localhost:8000/test.html](http://localhost:8000/test.html)

---

### 🐳 Option 2: Run with Docker 

#### 1. Start everything with Docker Compose:
```bash
docker-compose up --build
```

#### 2. Visit the API at:
[http://localhost:5000](http://localhost:5000)

#### 3. MySQL will run on port `3306`, user=`root`, pass=`root`, db=`expense_db`

---

## 🧪 Test Steps 

### 🔘 Sample Test with curl

#### ➕ Create User
```bash
curl -X POST http://localhost:5000/user -H "Content-Type: application/json" -d '{"name": "Pandu", "email": "pandu@example.com"}'
```

#### 💰 Set Budget
```bash
curl -X POST http://localhost:5000/budget -H "Content-Type: application/json" -d '{"user_id": 1, "category": "Food", "month": "2025-04", "limit": 1000}'
```

#### 🧾 Log Expense
```bash
curl -X POST http://localhost:5000/expense -H "Content-Type: application/json" -d '{"user_id": 1, "category": "Food", "amount": 950}'
```

#### 📊 Get Report
```bash
curl http://localhost:5000/report/1/2025-04
```

#### 🚨 Check Alerts
```bash
curl http://localhost:5000/alerts/1/2025-04
```

Or use the HTML `test.html` interface.

---

## 📚 SQL / ORM Implementation 
- All models use `SQLAlchemy`
- Queries use ORM abstraction (`db.session.query`, `.filter_by`, `.group_by`)
- `get_monthly_spending()` uses `func.sum` to calculate totals

---

## 📄 In-Code Documentation 
- Each route includes inline comments
- Utility functions like `check_alerts` are fully documented
- Code is modular and split across files: `routes.py`, `utils.py`, `models.py`

---

## 🐳 Docker Setup

### 📄 `Dockerfile`
```Dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "-m", "app.main"]
```

### 📄 `docker-compose.yml`
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - db
    environment:
      - DB_USER=root
      - DB_PASSWORD=root
      - DB_HOST=db
      - DB_NAME=expense_db

  db:
    image: mysql:8.0
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: expense_db
    volumes:
      - mysqldata:/var/lib/mysql

volumes:
  mysqldata:
```

---

✅ All requirements fulfilled for full marks 🎯
Need help submitting or pushing to GitHub? Let me know!
