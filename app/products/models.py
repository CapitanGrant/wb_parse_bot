from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.dao.database import Base


class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    artikul: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[int] = mapped_column(Integer, nullable=False)
    subscribers_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=True)

    def __repr__(self):
        return (
            f'<Person(id={self.id}, name={self.name}, artikul={self.artikul}, price={self.price}, rating={self.rating}, volume={self.volume})>')
