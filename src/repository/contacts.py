from typing import List, Optional
from datetime import date, timedelta

from sqlalchemy import and_, or_, extract
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactBase, ContactUpdate


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def create_contact(body: ContactBase, user: User, db: Session) -> Contact:    
    contact = Contact(name=body.name, surname = body.surname, email = body.email, phone = body.phone, birth_date = body.birth_date, additional_data = body.additional_data, user = user)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactUpdate, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        if body.name is not None:
            contact.name = body.name
        if body.surname is not None:
            contact.surname = body.surname
        if body.email is not None:
            contact.email = body.email
        if body.phone is not None:
            contact.phone = body.phone
        if body.birth_date is not None:
            contact.birth_date = body.birth_date
        if body.additional_data is not None:
            contact.additional_data = body.additional_data
        db.commit()
        db.refresh(contact)
    return contact

async def search_contacts(name: Optional[str], surname: Optional[str], email: Optional[str], user: User, db: Session) -> List[Contact]:
    query = db.query(Contact).filter(Contact.user_id == user.id)
    if name:
        query = query.filter(Contact.name.ilike(f"%{name}%"))
    if surname:
        query = query.filter(Contact.surname.ilike(f"%{surname}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    return query.all()

async def get_upcoming_birthdays(user: User, db: Session) -> List[Contact]:
    today = date.today()
    next_week = today + timedelta(days=7)
    
    # Extract the day and month parts of today's date and the next week's date
    today_month_day = (today.month, today.day)
    next_week_month_day = (next_week.month, next_week.day)

    if today_month_day <= next_week_month_day:
        # The dates are within the same calendar year
        return db.query(Contact).filter(
            and_(
                extract('month', Contact.birth_date).between(today.month, next_week.month),
                extract('day', Contact.birth_date).between(today.day, next_week.day),
                Contact.user_id == user.id
            )
        ).all()
    else:
        # The dates span the end of the year and the beginning of the next year
        return db.query(Contact).filter(
            and_(
                Contact.user_id == user.id,
                or_(
                    and_(
                        extract('month', Contact.birth_date) == today.month,
                        extract('day', Contact.birth_date) >= today.day
                    ),
                    and_(
                        extract('month', Contact.birth_date) == next_week.month,
                        extract('day', Contact.birth_date) <= next_week.day
                    ),
                    and_(
                        extract('month', Contact.birth_date) > today.month,
                        extract('month', Contact.birth_date) < next_week.month
                    )
                )
            )
        ).all()