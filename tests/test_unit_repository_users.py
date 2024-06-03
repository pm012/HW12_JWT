import unittest
from unittest.mock import MagicMock, AsyncMock

from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email, create_user, update_token, confirmed_email, update_avatar
)

class TestUsersRepository(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.db = MagicMock(spec=Session)
        self.user = User(id=1, email="test@example.com")
        self.user_model = UserModel(email="test@example.com", password="password123")

    async def test_get_user_by_email(self):
        self.db.query().filter().first.return_value = self.user
        result = await get_user_by_email(email="test@example.com", db=self.db)
        self.db.query().filter().first.assert_called_once()
        self.assertEqual(result, self.user)

    async def test_create_user(self):
        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()
        result = await create_user(body=self.user_model, db=self.db)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        self.assertIsInstance(result, User)

    async def test_update_token(self):
        self.db.commit = MagicMock()
        await update_token(user=self.user, token="newtoken", db=self.db)
        self.assertEqual(self.user.refresh_token, "newtoken")
        self.db.commit.assert_called_once()

    async def test_confirmed_email(self):
        self.db.query().filter().first.return_value = self.user
        self.db.commit = MagicMock()
        await confirmed_email(email="test@example.com", db=self.db)
        self.assertTrue(self.user.confirmed)
        self.db.commit.assert_called_once()

    async def test_update_avatar(self):
        self.db.query().filter().first.return_value = self.user
        self.db.commit = MagicMock()
        result = await update_avatar(email="test@example.com", url="http://new.avatar.url", db=self.db)
        self.assertEqual(self.user.avatar, "http://new.avatar.url")
        self.db.commit.assert_called_once()
        self.assertEqual(result, self.user)

if __name__ == '__main__':
    unittest.main()
