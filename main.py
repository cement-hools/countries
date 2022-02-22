import json
from typing import List

import fastapi
from unidecode import unidecode
from fastapi import HTTPException, Request
from pydantic import parse_obj_as

from schemas import Country, Countries, City, CountryWithCity

app = fastapi.FastAPI()

url = "https://api.countrystatecity.in/v1/countries"

with open('db/countries.json', encoding='utf-8') as f:
    COUNTRIES = json.load(f)

with open('db/states.json', encoding='utf-8') as f:
    STATES = json.load(f)

with open('db/cities.json', encoding='utf-8') as f:
    CITIES = json.load(f)


@app.get('/api/v1/countries', response_model=List[Countries])
def countries():
    result = COUNTRIES

    return result


@app.get('/api/v1/countries/{country_code}', response_model=Country)
def country(country_code: str):
    countries_dict: dict = {item["iso2"]: item for item in COUNTRIES}

    country_code: str = country_code.upper()
    country_item = countries_dict.get(country_code)

    if country_item:
        return country_item

    raise HTTPException(status_code=404, detail="Item not found")


@app.get('/api/v1/cities', response_model=List[City])
def cities(request: Request):
    request_args = dict(request.query_params)

    result = []
    filter_name: str = request_args.get("name")
    if filter_name:
        filter_name = filter_name.lower()

        exists_city = ""
        for item in CITIES:
            city_name: str = item["name"].lower()
            if (
                    city_name.startswith(filter_name) or
                    unidecode(city_name).startswith(filter_name)
            ):

                if exists_city == city_name.split()[0]:
                    continue
                else:
                    exists_city = city_name.split()[0]

                result.append(item)
        return result
    return CITIES


@app.get('/api/v2/cities',
         response_model=List[CountryWithCity]
         )
def cities_v2(request: Request):
    request_args = dict(request.query_params)

    filter_name: str = request_args.get("name")
    if filter_name:
        filter_name = filter_name.lower()

        countries = {}

        for item in CITIES:
            city_name: str = item["name"].lower()
            if (
                    city_name.startswith(filter_name) or
                    unidecode(city_name).startswith(filter_name)
            ):
                # print(unidecode(city_name))
                cities_list: list = countries.get((item["country_code"]), [])
                cities_list.append(item)
                countries[item["country_code"]] = cities_list

        result = []
        for k, v in countries.items():
            item = {"country": k, "cities": v, "count_cities": len(v)}
            result.append(item)

        return result

    raise HTTPException(status_code=400, detail="Bad Reques")


@app.get('/api/v1/check', response_model=List[Country])
def check(request: Request):
    request_args = dict(request.query_params)
    result = []
    filter_name: str = request_args.get("name")
    if filter_name:
        filter_name = filter_name.lower()

        for item in COUNTRIES:
            country_name: str = item["name"].lower()
            if country_name.startswith(filter_name):
                result.append(item)

    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
