from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from . import database
from sqlalchemy.orm import relationship


class TicketPurchase(database.Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    concert_id = Column(Integer, ForeignKey("concerts.id"))  # Link to the concert
    user_email = Column(String)

    # Relationship allows you to access concert info from a ticket
    concert = relationship("Concert", back_p_populates="tickets")


class Concert(database.Base):
    __tablename__ = "concerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    total_capacity = Column(Integer)  # How many exist in total

    # This lets you do: my_concert.tickets to see all sold ones
    tickets = relationship("TicketPurchase", back_populates="concert")