from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db_manager import Base

class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    members = relationship('User', back_populates='teams')

    def __repr__(self):
        return f"<Team(id={self.id}, name='{self.name}', owner_id={self.owner_id})>"