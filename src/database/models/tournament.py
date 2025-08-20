from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db_manager import Base

class Tournament(Base):
    __tablename__ = 'tournaments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)

    creator = relationship("User", back_populates="tournaments")

    def __repr__(self):
        return f"<Tournament(name={self.name}, start_date={self.start_date}, end_date={self.end_date})>"