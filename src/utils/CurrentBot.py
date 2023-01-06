from src.location_handling.regions.abstract_region import AbstractRegion


class CurrentBot:
    id = 0
    location = 0
    region: AbstractRegion = None