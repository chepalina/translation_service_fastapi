"""
SQL Alchemy models declaration.
https://docs.sqlalchemy.org/en/14/orm/declarative_styles.html#example-two-dataclasses-with-declarative-table
Dataclass style for powerful autocompletion support.

https://alembic.sqlalchemy.org/en/latest/tutorial.html
Note, it is used by alembic migrations logic, see `alembic/env.py`

Alembic shortcuts:
# create migration
alembic revision --autogenerate -m "migration_name"

# apply all migrations
alembic upgrade head
"""
import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_model"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    email: Mapped[str] = mapped_column(
        String(254), nullable=False, unique=True, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)


from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class Word(Base):
    __tablename__ = "words"
    word_id = Column(Integer, primary_key=True)
    word = Column(Text, nullable=False)
    language = Column(String(50), nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow)

    # Relationships
    definitions = relationship("Definition", back_populates="word")
    synonyms = relationship("Synonym", back_populates="word")
    translations = relationship("Translation", back_populates="word")
    examples = relationship("Example", back_populates="word")


class Definition(Base):
    __tablename__ = "definitions"
    definition_id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey("words.word_id"))
    language = Column(String(50), nullable=False)
    definition = Column(Text, nullable=False)

    # Relationship
    word = relationship("Word", back_populates="definitions")


class Synonym(Base):
    __tablename__ = "synonyms"
    synonym_id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey("words.word_id"))
    language = Column(String(50), nullable=False)
    synonym = Column(Text, nullable=False)

    # Relationship
    word = relationship("Word", back_populates="synonyms")


class Translation(Base):
    __tablename__ = "translations"
    translation_id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey("words.word_id"))
    language = Column(String(50), nullable=False)
    translation = Column(Text, nullable=False)

    # Relationship
    word = relationship("Word", back_populates="translations")


class Example(Base):
    __tablename__ = "examples"
    example_id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey("words.word_id"))
    language = Column(String(50), nullable=False)
    example = Column(Text, nullable=False)

    # Relationship
    word = relationship("Word", back_populates="examples")
