from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.functions import hash_password
from app.models.User import User
from app.schemas.User import UserCreate
from typing import Optional


def create_user(db: Session, data: UserCreate) -> User:
    """
    Creates a new user in the database. This function checks for the existence
    of a user with the same username and, if not found, hashes the provided
    password and saves a new user record in the database.

    :param db: The database session used for querying and storing data.
    :type db: Session
    :param data: An object containing the user's details necessary for
        creation, such as username and password.
    :type data: UserCreate
    :return: The newly created user object after being committed to the
        database and refreshed.
    :rtype: User
    """
    existing_user = db.query(User).filter(User.username == data.username).first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El usuario ya existe")

    hashed_password = hash_password(data.password)
    new_user = User(
        username=data.username,
        hashed_password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def create_admin_user(db: Session, data: UserCreate) -> User:
    """
    Creates an administrative user with the given user data. This function utilizes
    the `create_user` function to create a base user, then promotes the user to an
    admin by setting the `is_admin` attribute to `True`. The changes are persisted
    to the database, and the refreshed user object is returned.

    :param db: Database session object, which is used to perform operations
        on the database.
    :type db: Session

    :param data: The user creation data object, typically containing fields such
        as username, password, and other user-specific details.
    :type data: UserCreate

    :return: A `User` object representing the newly created admin user.
    :rtype: User
    """
    new_user = create_user(db, data)
    new_user.is_admin = True
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(db: Session, user_id: int, force_status: Optional[bool] = None, search_deleted: bool = False) -> User:
    """
    Retrieve a user from the database based on their ID, with optional status
    validation and an option to search for deleted users. Additional checks
    can be performed based on whether a user is marked as deleted or not.

    :param db: Database session object used to execute queries.
    :param user_id: The ID of the user to retrieve.
    :param force_status: Optional. A boolean value used to force validation of the user's
        deletion status. If set to True, an exception is raised if the user is marked
        as deleted. If set to False, an exception is raised if the user is not marked
        as deleted.
    :param search_deleted: A boolean indicating whether deleted users should be queried.
        If False, and the user is deleted, the function will raise an exception.
    :return: The user object retrieved from the database.
    :rtype: User
    :raises HTTPException: Raised if the user is not found, or if any status-related
        validation conflicts occur based on the parameters provided.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario no existe"
        )
    if force_status is not None:
        if force_status and user.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El usuario ya fue eliminado"
            )
        if not force_status and not user.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El usuario no estaba eliminado"
            )

    if user.is_deleted and not search_deleted:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuario ya fue eliminado"
        )

    return user


def delete_user(db: Session, user_id: int) -> User:
    """
    Deletes a user by marking the `is_deleted` attribute as True in the database.
    The user entity is fetched using the provided user_id. The changes are committed
    and refreshed in the session before returning the updated user instance.

    :param db: Database session used for fetching and updating the user data.
    :type db: Session
    :param user_id: Identifier for the user to be deleted.
    :type user_id: int
    :return: The updated user instance with the `is_deleted` attribute set to True.
    :rtype: User
    """
    user = get_user(db, user_id, force_status=True)
    user.is_deleted = True
    db.commit()
    db.refresh(user)
    return user


def restore_user(db: Session, user_id: int) -> User:
    """
    Restores a deleted user in the database by setting the `is_deleted` flag to False.
    The function retrieves the user using the provided user ID, updates the deleted status,
    and commits the changes to the database.

    :param db: The database session used to interact with the database.
    :type db: Session
    :param user_id: The ID of the user to be restored.
    :type user_id: int
    :return: The updated user instance with the `is_deleted` flag set to False.
    :rtype: User
    """
    user = get_user(db, user_id, force_status=False, search_deleted=True)
    user.is_deleted = False
    db.commit()
    db.refresh(user)
    return user

def change_password(db: Session, user_id:int, new_password:str):
    """
    Changes the password of a user in the database. This function retrieves the
    user by their user ID, hashes the new password, updates the user's password
    with the hashed value, commits the change to the database, and refreshes the
    user instance.

    :param db: Database session used to access the user table and perform the
        necessary updates.
    :type db: Session
    :param user_id: The unique identifier of the user whose password needs to be
        changed.
    :type user_id: int
    :param new_password: The new plain text password to be hashed and stored for
        the user.
    :type new_password: str
    :return: The updated user instance, after the password has been changed and
        refreshed in the database.
    :rtype: User
    """
    user = get_user(db,user_id)
    new_hashed_password = hash_password(new_password)
    user.hashed_password = new_hashed_password
    db.commit()
    db.refresh(user)
    return user