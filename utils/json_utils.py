import json
from typing import Any, Callable, List
from utils.types import Condition, Action, Rule, RelativeTime, ActionParameters

class JSONUtils:

    @staticmethod
    def read(file_path: str) -> Any:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in file {file_path}: {e}")

    @staticmethod
    def write(file_path: str, data: Any, pretty: bool = True) -> None:
        with open(file_path, "w", encoding="utf-8") as file:
            if pretty:
                json.dump(data, file, indent=2, ensure_ascii=False)
            else:
                json.dump(data, file, separators=(",", ":"), ensure_ascii=False)

    @staticmethod
    def update(file_path: str, update_func: Callable[[Any], Any]) -> None:
        data = JSONUtils.read(file_path)
        updated_data = update_func(data)
        JSONUtils.write(file_path, updated_data)

    @staticmethod
    def print_pretty(data: Any) -> None:
        """Pretty-prints JSON data to stdout."""
        print(json.dumps(data, indent=2, ensure_ascii=False))

    @staticmethod
    def parse_rules(json_data: List[dict]) -> List[Rule]:
        rules = []
        for item in json_data:
            conditions = []
            for cond in item["conditions"]:
                cond_copy = cond.copy()
                if isinstance(cond_copy["value"], dict):
                    cond_copy["value"] = RelativeTime(**cond_copy["value"])
                conditions.append(Condition(**cond_copy))

            actions = []
            for act in item["actions"]:
                parameters = ActionParameters(**act["parameters"])
                actions.append(Action(type=act["type"], parameters=parameters))

            rule = Rule(
                logic=item["logic"],
                conditions=conditions,
                actions=actions,
                description=item["description"]
            )
            rules.append(rule)
        return rules

