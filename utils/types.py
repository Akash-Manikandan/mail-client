from dataclasses import dataclass
from typing import List, Union, Literal, Optional


@dataclass
class RelativeTime:
    quantity: int
    unit: str


@dataclass
class Condition:
    field: str
    operator: str
    value: Union[str, RelativeTime]


@dataclass
class ActionParameters:
    status: Optional[str] = None
    destination: Optional[str] = None


@dataclass
class Action:
    type: str
    parameters: ActionParameters


@dataclass
class Rule:
    logic: Literal["all", "any"]
    conditions: List[Condition]
    actions: List[Action]
    description: str
