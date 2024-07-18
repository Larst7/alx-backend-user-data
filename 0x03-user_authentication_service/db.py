#!/usr/bin/env python3
""" represents the DB module"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """the DB class"""

    def __init__(self) -> None:
        """initializer for DB"""
        self._engine = create_engine("sqlite:///a.db",
                                     echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """session property"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """implements the user object """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """function finds all users"""
        total_users = self._session.query(User)
        for key, val in kwargs.items():
            if key not in User.__dict__:
                raise InvalidRequestError
            for userr in total_users:
                if getattr(userr, key) == val:
                    return userr
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """updates the user attributes"""
        try:
            uesr = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError()
        for key, val in kwargs.items():
            if hasattr(uesr, key):
                setattr(uesr, key, val)
            else:
                raise ValueError
        self._session.commit()
