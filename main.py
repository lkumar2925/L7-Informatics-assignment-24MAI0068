from flask import Blueprint, request, jsonify
from .database import db
from .models import User, Budget, Expense, Group, GroupMember, SharedExpense
from .utils import get_monthly_spending, check_alerts
from datetime import datetime

routes = Blueprint('routes', __name__)

@routes.route("/")
def home():
    return "✅ Expense Tracker API is running!"


@routes.route('/user', methods=['POST'])
def create_user():
    data = request.json
    user = User(name=data['name'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify({ "id": user.id, "name": user.name })

@routes.route('/budget', methods=['POST'])
def set_budget():
    data = request.json
    b = Budget(
        user_id=data['user_id'],
        category=data['category'],
        month=data['month'],
        limit=data['limit']
    )
    db.session.add(b)
    db.session.commit()
    return jsonify({ "status": "Budget added." })

@routes.route('/expense', methods=['POST'])
def add_expense():
    data = request.json
    e = Expense(
        user_id=data['user_id'],
        category=data['category'],
        amount=data['amount']
    )
    db.session.add(e)
    db.session.commit()
    return jsonify({ "status": "Expense logged." })

@routes.route('/report/<int:user_id>/<month>')
def report(user_id, month):
    data = get_monthly_spending(user_id, month)
    return jsonify(data)

@routes.route('/alerts/<int:user_id>/<month>')
def alerts(user_id, month):
    alert_msgs = check_alerts(user_id, month)
    return jsonify(alert_msgs)

# Group features
@routes.route('/group', methods=['POST'])
def create_group():
    g = Group(name=request.json['name'])
    db.session.add(g)
    db.session.commit()
    return jsonify({ "group_id": g.id })

@routes.route('/group/member', methods=['POST'])
def add_member():
    m = GroupMember(**request.json)
    db.session.add(m)
    db.session.commit()
    return jsonify({ "status": "Member added." })

@routes.route('/group/expense', methods=['POST'])
def add_shared_expense():
    e = SharedExpense(
        group_id=request.json['group_id'],
        paid_by=request.json['paid_by'],
        amount=request.json['amount'],
        description=request.json['description']
    )
    db.session.add(e)
    db.session.commit()
    return jsonify({ "status": "Shared expense added." })

@routes.route('/group/settle/<int:group_id>')
def settle_group(group_id):
    members = GroupMember.query.filter_by(group_id=group_id).all()
    expenses = SharedExpense.query.filter_by(group_id=group_id).all()

    balances = {m.user_id: 0 for m in members}
    for e in expenses:
        share = e.amount / len(members)
        for m in members:
            if m.user_id == e.paid_by:
                balances[m.user_id] += e.amount - share
            else:
                balances[m.user_id] -= share

    return jsonify({ str(uid): round(balance, 2) for uid, balance in balances.items() })
