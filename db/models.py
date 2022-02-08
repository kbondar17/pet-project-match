from db.session import create_db
from typing import Any

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from db.session import Base


class User(Base):
    __tablename__ = 'users'

    uid = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    user_name = Column(String, index=True)

    gender = Column(Integer)
    prog_lang = Column(String)
    self_description = Column(String)
    project_description = Column(String)
    has_seen = Column(String)
    was_shown_to = Column(String)
    profile_pic = Column(Boolean)
    tag = Column(String)

    def __repr__(self) -> str:
        return f'User {self.name} {self.uid}'


class WhoSeenWho(Base):
    __tablename__ = 'who_seen_who'

    uid = Column(Integer, primary_key=True)
    who = Column(Integer, ForeignKey(User.uid, ondelete='CASCADE'), index=True)
    seen_who = Column(Integer)

    __table_args__ = (
        UniqueConstraint(who, seen_who),
    )

    def __repr__(self) -> str:
        return f'User {self.uid} has seen {self.who}'

if __name__ == '__main__':
    create_db()

class WhoLikedWho(Base):
    __tablename__ = 'who_liked_who'

    uid = Column(Integer, primary_key=True)
    who = Column(Integer, ForeignKey(User.uid, ondelete='CASCADE'), index=True)
    liked_who = Column(Integer)
    liked_person_notificated = Column(Boolean)

    __table_args__ = (
        UniqueConstraint(who, liked_who),
    )

    def __repr__(self) -> str:
        return f'User {self.who} liked {self.liked_who}'


if __name__ == '__main__':
    create_db()

