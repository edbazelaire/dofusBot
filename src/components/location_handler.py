from src.entity.city.astrub import AbstractCity


class LocationHandler:
    def __init__(self, farm_region: str, city: AbstractCity):
        self.farm_region = farm_region
        self.city = city

