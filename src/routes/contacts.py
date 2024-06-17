"""
This module defines the contact management routes for a FastAPI application.
It includes endpoints for reading, searching, creating, updating, and deleting contacts,
as well as retrieving contacts with upcoming birthdays.
"""

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.models import User
from src.database.db import get_db
from src.schemas import ContactBase, ContactResponse, ContactUpdate
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])

@router.get("/", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), 
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve a list of contacts with pagination.

    - **skip**: Number of contacts to skip.
    - **limit**: Maximum number of contacts to retrieve.
    - **db**: Database session dependency.
    - **current_user**: Current authenticated user.

    Returns a list of contacts.
    """
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts

@router.get("/search", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def search_contacts(
    name: Optional[str] = Query(None),
    surname: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Search for contacts by name, surname, or email.

    - **name**: Name of the contact to search for.
    - **surname**: Surname of the contact to search for.
    - **email**: Email of the contact to search for.
    - **current_user**: Current authenticated user.
    - **db**: Database session dependency.

    Returns a list of contacts matching the search criteria.
    """
    contacts = await repository_contacts.search_contacts(name, surname, email, current_user, db)
    return contacts

@router.get("/birthdays", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_upcoming_birthdays(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve contacts with upcoming birthdays.

    - **db**: Database session dependency.
    - **current_user**: Current authenticated user.

    Returns a list of contacts with upcoming birthdays.
    """
    contacts = await repository_contacts.get_upcoming_birthdays(current_user, db)
    return contacts

@router.get("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contact(contact_id: int, 
                       db: Session = Depends(get_db), 
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve a specific contact by ID.

    - **contact_id**: ID of the contact to retrieve.
    - **db**: Database session dependency.
    - **current_user**: Current authenticated user.

    Returns the contact details.
    """
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.post("/", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))], status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactBase, 
                         current_user: User = Depends(auth_service.get_current_user),  
                         db: Session = Depends(get_db)):
    """
    Create a new contact.

    - **body**: ContactBase object containing contact details.
    - **current_user**: Current authenticated user.
    - **db**: Database session dependency.

    Returns the created contact details.
    """
    return await repository_contacts.create_contact(body, current_user, db)

@router.patch("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact(contact_id: int, 
                         body: ContactUpdate, 
                         current_user: User = Depends(auth_service.get_current_user), 
                         db: Session = Depends(get_db)):
    """
    Update an existing contact by ID.

    - **contact_id**: ID of the contact to update.
    - **body**: ContactUpdate object containing updated contact details.
    - **current_user**: Current authenticated user.
    - **db**: Database session dependency.

    Returns the updated contact details.
    """
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="contact not found")
    return contact

@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, 
                         current_user: User = Depends(auth_service.get_current_user), 
                         db: Session = Depends(get_db)):
    """
    Delete a contact by ID.

    - **contact_id**: ID of the contact to delete.
    - **current_user**: Current authenticated user.
    - **db**: Database session dependency.

    Returns the details of the deleted contact.
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
