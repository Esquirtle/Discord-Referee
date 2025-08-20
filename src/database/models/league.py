from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class League(Base):
    __tablename__ = 'leagues'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    season = Column(String, nullable=False)
    max_teams = Column(Integer, nullable=False)
    current_teams = Column(Integer, default=0)

    # Relationships
    teams = relationship("Team", back_populates="league")

    def __repr__(self):
        return f"<League(id={self.id}, name='{self.name}', season='{self.season}', max_teams={self.max_teams})>"