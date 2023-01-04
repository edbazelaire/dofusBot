from typing import List

from src.buildings.Bank import Bank
from src.enum.jobs import Jobs
from src.enum.ressources import Ressources
from src.utils.ErrorHandler import ErrorHandler


class Craft:
    CRAFTS = {
        Jobs.PAYSAN: {
            Ressources.BRIOCHETTE: {
                Ressources.HOUBLON: 5,
                Ressources.TREFLES: 1,
                Ressources.CENDRES_ETERNELLES: 1
            },

            Ressources.PAIN_D_INCARNAM: {
                Ressources.BLE: 4
            }
        },

        Jobs.BUCHERON: {}
    }

    def __init__(self, craft_names: List[str]):
        self.crafts = {craft_name: self.get_recipe(craft_name) for craft_name in craft_names}         # list of available crafts
        self.craft_order = None     # name of the craft to do

        # say that player has craft requests or not
        self.is_crafting = craft_names is not None and len(craft_names) > 0

    def transfer_required_ressources(self):
        """ get ressources from bank necessary to crafts """
        self.craft_order = None

        for craft_name, recipe in self.crafts.items():
            # search recipe
            success = Bank.search_recipe(craft_name)
            if not success:
                continue

            # transfer ressources
            success = Bank.transfer_recipe()
            if not success:
                ErrorHandler.error("recipe found but unable to transfer")
                continue

            # set craft order and return
            print("CRAFT ORDER SET : " + craft_name)
            self.craft_order = craft_name
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
        # return self.max_pods // req_pods
        return 0    # not using max pods for now

    @staticmethod
    def get_recipe(craft_name: str):
        for crafts in Craft.CRAFTS.values():
            if craft_name in crafts.keys():
                return crafts[craft_name]

        ErrorHandler.fatal_error(f"recipe not found : {craft_name}")

    @staticmethod
    def get_job(craft_name: str):
        for job, crafts in Craft.CRAFTS.items():
            if craft_name in crafts.keys():
                return job

        ErrorHandler.fatal_error(f"job not found for : {craft_name}")

