"""
Move this file to the flask_paralympics package for activity 7.3

The 'db' parameter is defined during activity 7.2.

Complete the code for the quiz tables at the end of the models.py file."""
from typing import List

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tutor.student import db


# Note: db.Model is the declarative base class for SQLAlchemy that was defined in the __init__.py file
class Event(db.Model):
    __tablename__ = 'event'
    event_id = mapped_column(Integer, primary_key=True)
    type = mapped_column(Text, nullable=False)
    year = mapped_column(Integer, nullable=False)
    start: Mapped[Optional[str]] = mapped_column(Text)  # Different syntax to show the difference
    end = mapped_column(Text)
    duration = mapped_column(Integer)
    countries = mapped_column(Integer)
    events = mapped_column(Integer)
    sports = mapped_column(Integer)
    highlights = mapped_column(Text)
    url = mapped_column(Text)

    # Relationships - one-to-many:
    host_events: Mapped[List["HostEvent"]] = relationship(back_populates="event")
    disability_events: Mapped[List["DisabilityEvent"]] = relationship(back_populates="event")
    medal_results: Mapped[List["MedalResult"]] = relationship(back_populates="event")
    questions: Mapped[List["Question"]] = relationship(back_populates="event")
    # one-to-one relationship:
    participants: Mapped["Participants"] = relationship(back_populates="event")


class Country(db.Model):
    """
    Represents a country in the database.

    Attributes:
        code (str): Primary key for the country.
        name (str): Name of the country.
        region (str): Region of the country.
        sub_region (str): Sub-region of the country.
        member_type (str): Type of team.
        notes (str): Additional notes about the country.
    """
    __tablename__ = 'country'

    code = mapped_column(Text, primary_key=True)
    name = mapped_column(Text, nullable=False)
    region = mapped_column(Text)
    sub_region = mapped_column(Text)
    member_type = mapped_column(Text)
    notes = mapped_column(Text)
    # Relationships
    medal_results: Mapped[List["MedalResult"]] = relationship(back_populates="country")
    hosts: Mapped[List["Host"]] = relationship(back_populates="country")


class Disability(db.Model):
    __tablename__ = 'disability'

    disability_id = mapped_column(Integer, primary_key=True)
    category = mapped_column(Text, nullable=False)
    # Relationship to the DisabilityEvent table. back_populates takes the name of the relationship that is defined in the DisabilityClass
    disability_events: Mapped[List["DisabilityEvent"]] = relationship(back_populates="disability")


class DisabilityEvent(db.Model):
    __tablename__ = 'disability_event'

    event_id: Mapped[int] = mapped_column(ForeignKey('event.event_id'), primary_key=True)
    disability_id: Mapped[int] = mapped_column(ForeignKey('disability.disability_id'), primary_key=True)

    # Relationships to the parent classes: Event and Disability
    # back_populates takes the name of the relationships that is defined in the parent classes (same name was used in both)
    event: Mapped["Event"] = relationship("Event", back_populates="disability_events")
    disability: Mapped["Disability"] = relationship("Disability", back_populates="disability_events")


class Host(db.Model):
    __tablename__ = 'host'

    host_id = mapped_column(Integer, primary_key=True)
    country_code = mapped_column(ForeignKey('country.code'))
    host = mapped_column(Text, nullable=False)

    # Relationships
    host_events: Mapped[List["HostEvent"]] = relationship(back_populates="host")
    country: Mapped["Country"] = relationship(back_populates="hosts")


class HostEvent(db.Model):
    __tablename__ = 'host_event'

    host_id = mapped_column(Integer,
                            ForeignKey('host.host_id', onupdate="CASCADE", ondelete="NO ACTION"),
                            primary_key=True
                            )
    event_id = mapped_column(Integer,
                             ForeignKey('event.event_id', onupdate="CASCADE", ondelete="NO ACTION"),
                             primary_key=True
                             )
    # Relationships
    event: Mapped["Event"] = relationship("Event", back_populates="host_events")
    host: Mapped["Host"] = relationship("Host", back_populates="host_events")


class Participants(db.Model):
    __tablename__ = 'participants'

    participant_id = mapped_column(Integer, primary_key=True)
    event_id = mapped_column(Integer, ForeignKey('event.event_id'))
    participants_m = mapped_column(Integer)
    participants_f = mapped_column(Integer)
    participants = mapped_column(Integer)

    # THis is a one-to-one relationship:
    event: Mapped["Event"] = relationship(back_populates="participants")


class MedalResult(db.Model):
    __tablename__ = 'medal_result'

    result_id = mapped_column(Integer, primary_key=True)
    event_id = mapped_column(Integer, ForeignKey('event.event_id'))
    country_code = mapped_column(Text, ForeignKey('country.code'))
    rank = mapped_column(Integer)
    gold = mapped_column(Integer)
    silver = mapped_column(Integer)
    bronze = mapped_column(Integer)
    total = mapped_column(Integer)
    # Relationships
    event: Mapped["Event"] = relationship(back_populates="medal_results")
    country: Mapped["Country"] = relationship(back_populates="medal_results")


class Quiz(db.Model):
    pass


class Question(db.Model):
    pass


class AnswerChoice(db.Model):
    pass


class QuizQuestion(db.Model):
    pass


class StudentResponse(db.Model):
    pass
