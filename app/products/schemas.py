from pydantic import BaseModel, Field


class SProduct(BaseModel):
    name: str = Field(..., description="Наименование товара")
    artikul: int = Field(..., description="Артикул товара")
    price: float = Field(..., description="Цена товара")
    rating: float = Field(..., description="Рейтинг товара")
    volume: int = Field(..., description="Количество товара")



class SProductArtikul(BaseModel):
    artikul: int

