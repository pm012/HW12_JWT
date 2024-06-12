import unittest
from unittest.mock import MagicMock, AsyncMock
from datetime import date, timedelta

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactBase, ContactUpdate
from src.repository.contacts import (
    get_contacts, 
    get_contact, 
    create_contact, 
    remove_contact, 
    update_contact, 
    search_contacts, 
    get_upcoming_birthdays
)

class TestContactsRepository(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.db = MagicMock(spec=Session)
        self.user = User(id=1, email="some@email.ua")        

    async def test_get_contacts(self):
        contacts = [
            Contact(email="contact1@example.com"),
            Contact(email="contact2@example.com"),
            Contact(email="contact3@example.com")
        ]
        
        self.db.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.db)  # type: ignore
        self.assertEqual(result, contacts)

    async def test_get_contact(self):
        contact = Contact(email="contact@example.com")
        self.db.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.db)
        self.db.query().filter().first.assert_called_once()
        self.assertEqual(result, contact)

    async def test_create_contact(self):

        contact = ContactBase(name='test', surname="test_surname", email="test@example.com", phone="123432", birth_date=date(1981, 6, 13))
        self.db.query().filter().all.return_value = contact        
        result = await create_contact(body=contact, user=self.user, db=self.db)
        self.assertEqual(result.surname, contact.surname)
        self.assertEqual(result.name, contact.name)
        self.assertEqual(result.email, contact.email)
        self.assertEqual(result.phone, contact.phone)
        self.assertEqual(result.birth_date, contact.birth_date)
        self.assertTrue(hasattr(result,'id'))

    async def test_remove_contact_found(self):
        contact = Contact(id=1)
        self.db.query().filter().first.return_value = contact        
        result = await remove_contact(contact_id=1, user=self.user, db=self.db)        
        self.assertEqual(result, contact)


    async def test_remove_contact_not_found(self):        
        self.db.query().filter().first.return_value = None        
        result = await remove_contact(contact_id=1, user=self.user, db=self.db)        
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        contact_upd = ContactUpdate(name='test_upd', surname="test_surname_upd", email="test_upd@example.com", phone="11111111", birth_date=date(1981, 6, 13))
        contact = Contact(name='test', surname="test_surname", email="test@example.com", phone="123432", birth_date=date(1981, 5, 12))
        self.db.query().filter().first.return_value = contact
        self.db.commit.return_value = None
        result = await update_contact(contact_id=1, body=contact_upd, user=self.user, db=self.db)        
        self.assertEqual(result.name, contact_upd.name)
        self.assertEqual(result.surname, contact_upd.surname)
        self.assertEqual(result.email, contact_upd.email)
        self.assertEqual(result.phone, contact_upd.phone)
        self.assertEqual(result.birth_date, contact_upd.birth_date)

    async def test_update_contact_not_found(self):
        contact_upd = ContactUpdate(name='test_upd', surname="test_surname_upd", email="test_upd@example.com", phone="11111111", birth_date=date(1981, 6, 13))
        self.db.query().filter().first.return_value = None
        self.db.commit.return_value = None
        result = await update_contact(contact_id=1, body=contact_upd, user=self.user, db=self.db)        
        self.assertIsNone(result)

    async def test_search_contacts(self):
        contacts = [
            Contact(name="John"),
            Contact(name = "Joe"),
            Contact(name="Joshoua")
        ]
        #self.db.query().filter().filter().all.return_value = contacts
        def mock_filter(*args, **kwargs):
            print(args)
            # Mocking filter logic
            name_filter = next((arg for arg in args if isinstance(arg, str) and "name" in arg), None)
            if name_filter and "%fake%" in name_filter:
                return MagicMock(all=MagicMock(return_value=[]))
            return MagicMock(all=MagicMock(return_value=contacts))

        query_mock = MagicMock()
        query_mock.filter.side_effect = mock_filter        
        self.db.query.return_value = query_mock
        result = await search_contacts(name="John", surname=None, email=None, user=self.user, db=self.db)
        for res in result:
            print(res.name)
            #self.assertEqual(res.name, "John")


    # async def test_get_upcoming_birthdays(self):
    #     today = date.today()
    #     next_week = today + timedelta(days=7)
    #     self.db.query().filter().all.return_value = []
    #     result = await get_upcoming_birthdays(user=self.user, db=self.db)
    #     self.db.query().filter().all.assert_called_once()
    #     self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
