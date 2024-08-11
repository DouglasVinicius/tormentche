import json

from utils.utils import json_names_normalization


class PreRunTasks:
    def __init__(self) -> None:
        self.pre_run_operations()

    def pre_run_operations(self) -> tuple[dict]:
        magic_file = open("data/magias.json")
        status_file = open("data/condicoes.json")
        maneuver_file = open("data/manobras.json")
        ally_file = open("data/parceiros.json")

        self.magic_json = json.loads(magic_file.read())
        self.status_json = json.loads(status_file.read())
        self.maneuver_json = json.loads(maneuver_file.read())
        self.ally_json = json.loads(ally_file.read())

        self.magic_json = json_names_normalization(self.magic_json)
        self.status_json = json_names_normalization(self.status_json)
        self.maneuver_json = json_names_normalization(self.maneuver_json)
        self.ally_json = json_names_normalization(self.ally_json)

        magic_file.close()
        status_file.close()
        maneuver_file.close()
        ally_file.close()
