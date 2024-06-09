import unittest
from unittest.mock import MagicMock, AsyncMock
from datetime import date, timedelta

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactBase, ContactUpdate
from src.repository.contacts import (
    get_contacts, get_contact, create_contact, remove_contact, update_contact, 
    search_contacts, get_upcoming_birthdays
)

class TestContactsRepository(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.db = MagicMock(spec=Session)
        self.user = User(id=1, email="some@email.ua")
        self.contact_base = ContactBase(
            name="John", surname="Doe", email="john.doe@example.com", 
            phone="1234567890", birth_date=date(1990, 1, 1), additional_data="Some info"
        )
        self.contact_update = ContactUpdate(
            name="John Updated", surname="Doe Updated", email="john.updated@example.com"
        )

    async def test_get_contacts(self):
        contacts = [
            Contact(email="contact1@example.com"),
            Contact(email="contact2@example.com"),
            Contact(email="contact3@example.com")
        ]
        print(f"Contacts: {contacts}")
        mock_query = self.db.query().filter_by().offset().limit()
        mock_query.all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.db)  # type: ignore
        print(f"Result: {result}")
        self.assertEqual([contact.email for contact in result], [contact.email for contact in contacts])

    async def test_get_contact(self):
        self.db.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.db)
        self.db.query().filter().first.assert_called_once()
        self.assertIsNone(result)

    async def test_create_contact(self):
        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()
        result = await create_contact(body=self.contact_base, user=self.user, db=self.db)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        self.assertIsInstance(result, Contact)

    async def test_remove_contact(self):
        contact = Contact(id=1)
        self.db.query().filter().first.return_value = contact
        self.db.delete = MagicMock()
        self.db.commit = MagicMock()
        result = await remove_contact(contact_id=1, user=self.user, db=self.db)
        self.db.query().filter().first.assert_called_once()
        self.db.delete.assert_called_once_with(contact)
        self.db.commit.assert_called_once()
        self.assertEqual(result, contact)

    async def test_update_contact(self):
        contact = Contact(id=1)
        self.db.query().filter().first.return_value = contact
        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()
        result = await update_contact(contact_id=1, body=self.contact_update, user=self.user, db=self.db)
        self.db.query().filter().first.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once_with(contact)
        self.assertEqual(result.name, self.contact_update.name)
        self.assertEqual(result.surname, self.contact_update.surname)
        self.assertEqual(result.email, self.contact_update.email)

    async def test_search_contacts(self):
        self.db.query().filter().filter().all.return_value = []
        result = await search_contacts(name="John", surname=None, email=None, user=self.user, db=self.db)
        self.db.query().filter().filter().all.assert_called_once()
        self.assertEqual(result, [])


    async def test_get_upcoming_birthdays(self):
        today = date.today()
        next_week = today + timedelta(days=7)
        self.db.query().filter().all.return_value = []
        result = await get_upcoming_birthdays(user=self.user, db=self.db)
        self.db.query().filter().all.assert_called_once()
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
