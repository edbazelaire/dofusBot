from src.entity.city.astrub import City


class LocationHandler:
    def __init__(self, farm_region: str, city: City):
        self.farm_region = farm_region
        self.city = city

