from .database import db
from .models import Expense, Budget, User
from sqlalchemy.sql import func
from .mailer import send_alert

def get_monthly_spending(user_id, month):
    results = db.session.query(
        Expense.category,
        func.sum(Expense.amount).label('total')
    ).filter(
        Expense.user_id == user_id,
        func.date_format(Expense.date, "%Y-%m") == month
    ).group_by(Expense.category).all()
    return {cat: float(total) for cat, total in results}

def check_alerts(user_id, month):
    try:
        user = User.query.get(user_id)
        spending = get_monthly_spending(user_id, month)
        budgets = Budget.query.filter_by(user_id=user_id, month=month).all()
        alerts = []

        for b in budgets:
            spent = spending.get(b.category, 0)
            if spent >= b.limit:
                msg = f"❌ Budget exceeded for {b.category} – Spent {spent}, Limit {b.limit}"
            elif spent >= 0.9 * b.limit:
                msg = f"⚠️ 90% used in {b.category} – Spent {spent}, Limit {b.limit}"
            else:
                continue

            alerts.append(msg)
            try:
                send_alert(user.email, "Budget Alert", msg)
            except Exception as e:
                print(f"[Mailer Error] {e}")

        return alerts

    except Exception as e:
        print(f"[check_alerts Error] {e}")
        return [f"Server error: {str(e)}"]

