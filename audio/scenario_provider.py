import json
from core.logger import logger

class ScenarioProvider:

    def __init__(self, filename):
        self._filename = filename
        self._data = self._load()

    def _load(self):
        with open(self._filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_scenarios(self):
        return self._data["scenarios"]

    def get_current(self):
        return self._data["current_scenario"]

    def set_current(self, name):
        if name not in self._data["scenarios"]:
            raise ValueError(f"Unknown scenario: {name}")

        self._data["current_scenario"] = name
        self._save()

    def get_scenario(self, name):
        return self._data["scenarios"][name]

    def _save(self):
        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump(
                self._data,
                f,
                ensure_ascii=False,
                indent=4
            )
    #   Returned list of tuples (scenario_id, caption) for all scenarios to be used in ListSelection widget
    def get_scenario_list(self):
        return [
            (scenario_id, scenario_data["caption"])
            for scenario_id, scenario_data in self.get_scenarios().items()
        ]
    def get_current_scenario_index(self):

        try:
            return next(
                i for i, (scenario_id, _) in enumerate(self.get_scenario_list())
                if scenario_id == self.get_current()
            )
        except:
            logger.error("wrong in scenarios.json current_scenario="+self.get_current())    
            return 0
