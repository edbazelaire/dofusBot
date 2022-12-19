import json


class JsonHandler:
    @staticmethod
    def get_json_path(ressources: list, region: str):
        with open('data/paths.json') as json_file:
            data = json.load(json_file)
            ressources.sort()
            name = '_'.join(ressources)
            if data is None or region not in data.keys() or name not in data[region].keys():
                return None
            return data[region][name]

    @staticmethod
    def save_json_path(ressources: list, region: str,  path: list):
        with open('data/paths.json', 'r') as json_file:
            all_paths = json.load(json_file)

        with open('data/paths.json', 'w') as json_file:
            ressources.sort()
            name = '_'.join(ressources)
            if region not in all_paths.keys():
                all_paths[region] = {}
            all_paths[region][name] = path
            json.dump(all_paths, json_file)