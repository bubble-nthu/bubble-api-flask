from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, Post

COUNT = 100

def users(count=COUNT):
    fake = Faker()
    i = 0
    while i < count:
        u = User(email=fake.email(),
            username=fake.user_name(),
            password='password',
            confirmed=True)

        u.profile.name = fake.name()
        u.profile.location = fake.city()
        u.profile.about_me = fake.text()
        u.profile.member_since = fake.past_date()
        
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()

def posts(count=COUNT):
    fake = Faker()
    user_count = User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        p = Post(body=fake.text(),
                timestamp=fake.past_date(),
                author=u)
        db.session.add(p)
    db.session.commit()
