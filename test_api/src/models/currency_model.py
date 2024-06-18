from pydantic import BaseModel



class CurrencyModel(BaseModel):
    NumCode: int
    CharCode: str
    Nominal: int
    Name: str
    Value: float
    VunitRate: float
