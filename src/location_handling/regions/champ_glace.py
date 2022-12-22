from src.enum.images import Images
from src.enum.regions import Regions
from src.enum.ressources import Ressources
from src.location_handling.city.Frigost import Frigost
from src.location_handling.regions.abstract_region import AbstractRegion


class ChampGlace(AbstractRegion):
    NAME: str = Regions.CHAMP_GLACE
    CITY = Frigost.NAME
    IS_REVERSE_PATH = True

    # LOCATIONS
    PHOENIX_STATUE_LOCATION: list = [-67, -44]
    CHECKPOINT: list = Frigost.ZAAP

    # ZONES
    ZONE_1 = [[-75, -50], [-68, -41]]

    RESSOURCES_LOCATIONS = {
        Ressources.FROSTIZ: [
            [-76, -47],
            [-77, -47],
            [-78, -47],
            [-72, -47],
            [-71, -47],
            [-71, -46],
            [-72, -46],
            [-73, -46],
            [-73, -45],
            [-74, -45],
            [-72, -45],
            [-71, -45],
            [-70, -45],
            [-72, -44],
            [-73, -44],
            [-71, -43],
            [-69, -42],
            [-70, -41],
            [-70, -40],
            [-69, -40],
            [-68, -40],
            [-68, -39],
            [-70, -39],
            [-69, -38],
            [-69, -37],
            [-70, -37],
            [-69, -35],
            [-71, -34],
            [-71, -33],
            [-72, -32],
        ]
    }

    # IMAGES
    PHOENIX_STATUE_IMAGE: str = Images.get(Images.PHOENIX_STATUE_3)

    def get_path(self, from_location, to_location):
        """ get path from a position to another (add special locations to go to if there is obstacle in between) """
        path = []
        # PRIORITISE Y MOVEMENT : in Zone 1
        if AbstractRegion.in_between(from_location, self.ZONE_1[0], self.ZONE_1[1]):
            if from_location[1] > to_location[1]:
                path.append([from_location[0], to_location[1]])

        # GOING TO CHECKPOINT
        elif from_location[1] > -47 >= to_location[1]:
            path.append([-70, -47])
        elif to_location[1] > -47 >= from_location[1]:
            path.append([-70, -47])

        path.append(to_location)
        return path
