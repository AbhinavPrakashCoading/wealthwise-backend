from app.core.db import SessionLocal, engine, Base
from app.models.models import User, Group, GroupMember, Expense, ExpenseSplit, Holding
from app.auth.security import get_password_hash

def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    # Users
    alice = User(email="alice@example.com", full_name="Alice", upi_id="alice@upi", hashed_password=get_password_hash("password"))
    bob = User(email="bob@example.com", full_name="Bob", upi_id="bob@upi", hashed_password=get_password_hash("password"))
    carol = User(email="carol@example.com", full_name="Carol", upi_id="carol@upi", hashed_password=get_password_hash("password"))
    db.add_all([alice, bob, carol])
    db.flush()
    # Group
    trip = Group(name="Goa Trip")
    db.add(trip)
    db.flush()
    db.add_all([GroupMember(group_id=trip.id, user_id=alice.id),
                GroupMember(group_id=trip.id, user_id=bob.id),
                GroupMember(group_id=trip.id, user_id=carol.id)])
    db.flush()
    # Expenses
    e1 = Expense(group_id=trip.id, payer_id=alice.id, amount=3000, description="Hotel")
    db.add(e1); db.flush()
    db.add_all([ExpenseSplit(expense_id=e1.id, user_id=alice.id, amount=1000),
                ExpenseSplit(expense_id=e1.id, user_id=bob.id, amount=1000),
                ExpenseSplit(expense_id=e1.id, user_id=carol.id, amount=1000)])
    e2 = Expense(group_id=trip.id, payer_id=bob.id, amount=900, description="Dinner")
    db.add(e2); db.flush()
    db.add_all([ExpenseSplit(expense_id=e2.id, user_id=alice.id, amount=300),
                ExpenseSplit(expense_id=e2.id, user_id=bob.id, amount=300),
                ExpenseSplit(expense_id=e2.id, user_id=carol.id, amount=300)])
    # Holdings (dummy)
    db.add_all([
        Holding(user_id=alice.id, type="stock", name="INFY", quantity=10, value=17000),
        Holding(user_id=alice.id, type="mutual_fund", name="Nifty Index Fund", quantity=100, value=25000),
        Holding(user_id=alice.id, type="bank", name="HDFC Savings", quantity=0, value=52000),
        Holding(user_id=alice.id, type="fd", name="SBI FD", quantity=0, value=100000),
    ])
    db.commit()
    db.close()
    print("Seeded sample data. Users: alice/bob/carol (password: password)")

if __name__ == "__main__":
    run()
