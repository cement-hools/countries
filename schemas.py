from typing import List, Optional

from pydantic import BaseModel, root_validator, validator


class RequestModel(BaseModel):
    city: str
    region: str
    country: str


class Countries(BaseModel):
    name: str
    iso3: str
    iso2: str
    # native: Optional[str]


class Country(Countries):
    phone_code: str
    capital: str
    region: str


class City(BaseModel):
    name: str
    state_code: str
    state_name: str
    country_code: str
    country_name: str


class CountryWithCity(BaseModel):
    country: str
    count_cities: int
    cities: List[City]

    # @validator("count_cities", always=True)
    # def composite_name(cls, v, values, **kwargs):
    #     cities = values['cities']
    #     return len(cities)
