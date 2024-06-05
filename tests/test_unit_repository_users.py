import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email, create_user, update_token, confirmed_email, update_avatar
)

class TestUsersRepository(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.db = MagicMock(spec=Session)
        self.user_model = UserModel(
            username="testuser",
            email="test@example.com",
            password="pass123"
        )
        self.user = User(
            id=1,
            username=self.user_model.username,
            email=self.user_model.email,
            password=self.user_model.password
        )

    async def test_get_user_by_email(self):
        self.db.query().filter().first.return_value = self.user
        result = await get_user_by_email(email=self.user_model.email, db=self.db)
        self.db.query().filter().first.assert_called_once()
        self.assertEqual(result, self.user)

    async def test_create_user(self):
        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()
        result = await create_user(body=self.user_model, db=self.db)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        self.assertEqual(result.email, self.user_model.email)

    async def test_update_token(self):
        new_token = "new_token"
        await update_token(user=self.user, token=new_token, db=self.db)
        self.db.commit.assert_called_once()
        self.assertEqual(self.user.refresh_token, new_token)

    async def test_confirmed_email(self):
        self.db.query().filter().first.return_value = self.user
        await confirmed_email(email=self.user_model.email, db=self.db)
        self.db.commit.assert_called_once()
        self.assertTrue(self.user.confirmed)

    async def test_update_avatar(self):
        new_avatar_url = "http://new-avatar-url.com"
        self.db.query().filter().first.return_value = self.user
        result = await update_avatar(email=self.user_model.email, url=new_avatar_url, db=self.db)
        self.db.commit.assert_called_once()
        self.assertEqual(result.avatar, new_avatar_url)

if __name__ == '__main__':
    unittest.main()
