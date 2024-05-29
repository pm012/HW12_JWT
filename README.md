# HW13_Backend

## Instructions

1. Apply HW12_JWT instructions (see below the HW13 tasks)
2. Sign up at least one user and add to this user at least one contact
3. To test CORS are enabled in terminal `cd /CORS_Testing -> ./run_server.sh` open http://localhost:3000/ authenticate and click the button to fetch contacts for user, then stop server (Ctrl+C) and run `./run_server_CORS_failure.sh`, open http://localhost:3001 authenticate -> In the developer console->Network tab error should be shown: "Response body is not available to scripts (Reason: CORS Missing Allow Origin)"

# Homework 13

## The first part

In this task, we continue to finalize the REST API application from homework 12.

### Tasks

1.  Implement the mechanism of verification of the registered user's email; (http://localhost:8000/docs#/auth/
2.  Request_email_api_auth_request_email_post)
3.  Limit the number of requests to your contact routes. Be sure to limit the speed - creating contacts for the user; (get contacts, and post create contacts are limited 10 requests per minute)
4.  Enable CORS for your REST API; Done - see instructions how to check above
5.  Implement the ability to update the user's avatar. Use Cloudinary service; Done PATCH /api/users/avatar - to update avatar, GET /api/users/me/ to load avatar from Cloudinary

### General requirements

1.  All environment variables must be stored in the file .env. Inside the code should not be confidential data in a “clean” form; Done
2.  Docker Compose is used to run all services and databases in the application; Done (2 services run)

### Additional task

1.  Implement the caching mechanism using the Redis database. Caching the current user during authorization; Not implemented!!!
2.  Implement the password reset mechanism for REST API application; Not implemented!!!

## The second part

see in HW10 Django

# HW12_JWT

## Instructions

1. Create and activate environment `python3.12 -m venv env`, `source /env/bin/activate`
2. Install libraries: `pip install -r requirements.txt`
3. Start PostgresDB: `docker-compose up -d`
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
