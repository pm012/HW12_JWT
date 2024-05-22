# HW12_JWT
initial database migration:
alembic init migrations
alembic revision --autogenerate -m 'Init'
alembic upgrade head

when database is changed:
alembic revision --autogenerate -m 'Auth_added_user'
alembic upgrade head

uvicorn main:app --host localhost --port 8000 --reload
