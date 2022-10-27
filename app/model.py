from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import SQL_URI


Base = declarative_base()
class Entry(Base):
    __tablename__ = 'entry'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    sugar = Column(Float)
    dosage = Column(Float)
    food = Column(Integer, nullable=True)
    brand = Column(String, nullable=True)
    water = Column(Integer, nullable=True)
    
    def __getitem__(self, key):
        if key in ("year", "month", "day", "hour", "minute"):
            return getattr(self.date, key)
        return getattr(self, key)

    def __repr__(self):
       return " ".join(map(str, (self.date,
                                 self.sugar,
                                 self.dosage,
                                 self.food,
                                 self.brand,
                                 self.water)))

engine = create_engine(SQL_URI)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()