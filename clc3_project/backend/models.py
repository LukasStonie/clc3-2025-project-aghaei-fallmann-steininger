from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import database  # Assumes database.py is in the same folder

class Concert(database.Base):
    __tablename__ = "concerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    date = Column(String)
    venue = Column(String)
    total_capacity = Column(Integer)

    # Relationship to tickets
    # Note: 'back_populates' must match the attribute name in TicketPurchase
    tickets = relationship("TicketPurchase", back_populates="concert")


class TicketPurchase(database.Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String)
    quantity = Column(Integer)

    # --- THE MISSING LINK ---
    # You must have a column that stores the ID of the concert.
    # ForeignKey("concerts.id") refers to the table name 'concerts' and column 'id'.
    concert_id = Column(Integer, ForeignKey("concerts.id"))

    # Relationship back to Concert
    concert = relationship("Concert", back_populates="tickets")