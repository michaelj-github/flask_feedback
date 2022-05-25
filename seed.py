from app import app
from models import db, User, Feedback

db.drop_all()
db.create_all()

u1 = User(
    username="user1",
    password="$2b$12$vuulJj603DUSU.YemqzKROY/XYROh8ki.mgRZqaalFZEEzeBcIy6u",
    email="user1@user1.com",
    first_name="User",
    last_name="One-User123U"
)

u2 = User(
    username="user2",
    password="$2b$12$vuulJj603DUSU.YemqzKROY/XYROh8ki.mgRZqaalFZEEzeBcIy6u",
    email="user2@user2.com",
    first_name="User",
    last_name="Two-User123U"
)

db.session.add_all([u1, u2])
db.session.commit()


f1 = Feedback(
    title="some feedback for user1",
    content="just some feedback for user1",
    username="user1"
)

f2 = Feedback(
    title="some feedback for user2",
    content="just some feedback for user2",
    username="user2"
)

db.session.add_all([f1, f2])
db.session.commit()


