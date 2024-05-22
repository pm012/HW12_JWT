import random
from datetime import date, timedelta
from faker import Faker
from sqlalchemy.orm import Session

from models import Base, Contact
from db import engine, SessionLocal

fake = Faker()

# Create tables (if they don't exist)
Base.metadata.create_all(bind=engine)

def create_fake_contact(birth_date):
    return Contact(
        name=fake.first_name(),
        surname=fake.last_name(),
        email=fake.email(),
        phone='+38(050)289-15-32', #fake.phone_number(),
        birth_date=birth_date,
        additional_data=fake.text(max_nb_chars=150),
        user_id = 2
    )

def populate_contacts(db: Session):
    today = date.today()
    next_week = today + timedelta(days=7)
    last_week = today - timedelta(days=7)

    # Generate contacts with birthdays within the next 7 days
    for _ in range(10):
        birth_date = today + timedelta(days=random.randint(0, 6)) - timedelta(days=random.randint(5, 40)*365)
        db.add(create_fake_contact(birth_date))

    # Generate contacts with birthdays before the last 7 days
    for _ in range(10):
        birth_date = last_week - timedelta(days=random.randint(1, 30))
        db.add(create_fake_contact(birth_date))

    # Generate contacts with birthdays after the next 7 days
    for _ in range(10):
        birth_date = next_week + timedelta(days=random.randint(1, 30))
        db.add(create_fake_contact(birth_date))

    db.commit()

def main():
    db = SessionLocal()
    try:
        populate_contacts(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()