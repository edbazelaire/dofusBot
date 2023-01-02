from src.buildings.Bank import Bank
from src.enum.ressources import Ressources


class Craft:
    CRAFTS = {
        Ressources.BRIOCHETTE: {
            Ressources.HOUBLON: 5,
            Ressources.TREFLES: 1,
            Ressources.CENDRES_ETERNELLES: 1
        },

        Ressources.PAIN_AMAKNA: {
            Ressources.BLE: 4
        }
    }

    def __init__(self, max_pods, crafts):
        self.max_pods = max_pods    # max pods of the player
        self.crafts = crafts        # list of available crafts
        self.craft_order = None     # name of the craft to do

        # say that player has craft requests or not
        self.is_crafting = crafts is not None and len(crafts) > 0

    def get_required_ressources(self):
        """ get ressources from bank necessary to crafts """
        for craft in self.crafts:
            n_crafts = self.get_n_possible_crafts(craft)

            if self.has_enough_ressources(craft, n_crafts):
                for ressource_name, qty in craft.items():
                    success = Bank.transfer(ressource_name, n=n_crafts * qty, from_bank=True)
                    if not success:
                        return False

                return True

        return False

    @staticmethod
    def has_enough_ressources(craft, n_crafts):
        for ressource_name, qty in craft.items():
            qty_in_bank = Bank.get_quantity_of(ressource_name)
            if qty_in_bank < n_crafts * qty:
                return False
        return True

    def get_n_possible_crafts(self, craft) -> int:
        # calculate pods requested to craft one item
        req_pods = 0
        for ressource_name, qty in craft.items():
            req_pods += qty * Ressources.get(ressource_name).pods

        # return max number of craft possible depending on max pods
        return self.max_pods // req_pods

