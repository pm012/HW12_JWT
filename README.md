# HW12_JWT

## Instructions

1. Create and activate environment "python3.12 -m venv env", "source /env/bin/activate"
2. Install libraries: "pip install -r requirements.txt"
3. Start PostgresDB: "docker-compose up -d"
4. Initial database migration(delete migrations folder before command run): `alembic init migrations`
5. In /migrations/env.py add: `from src.database.models import Base
                                 from src.database.db import SQLALCHEMY_DATABASE_URL`
   and replace
   `target_metadata = None`
   with
   `target_metadata = Base.metadata`
   `config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)`
6. Generate initial migration (Init - initial label)
   `alembic revision --autogenerate -m 'Init'`
7. Upgrade db and aply migration to db:
   `alembic upgrade head`

Note: when database is changed 4 step is not needed:
alembic revision --autogenerate -m 'Auth_added_user'
alembic upgrade head

8. Launch FastAPI: `uvicorn main:app --host localhost --port 8000 --reload` . Please find documentation on http://localhost:8000/docs
9. Authenticate and add couple 2 users (signup)
10. (Note set appropriate user id to bind contacts with added user). Generate database records (if needed after step 9). Launch /src/database/populate_db.py - to test nearest 7 days birthdays and binding contacts to appropriate users.

# Homework 12

In this home work, we'll continue to finalize our REST API application with homework 11.

## Tasks​

    implement the authentication mechanism in the application;
    implement the authorization mechanism using JWT tokens so that all contact transactions are carried out only by registered users;
    The user has access only to his operations with contacts;

## General requirements​

- When registering if the user already exists with such email, server will return error HTTP 409 Conflict;
- The server hashes the password and does not store it in an open form in the database;
- In case of successful user registration, the server must return HTTPResponse Status 201 Createdand data of a new user;
- For all operations POSTcreating a new resource, server returns status 201 Created;
- During the operation POST- user authentication, server accepts a request with user data (emailpassword) in the request body;
- If the user does not exist or the password does not match, the error returns HTTP 401 Unauthorized;
- Authorization mechanism with the help JWTtokens implemented by a pair of tokens: access token access_token and refresh token refresh_token

