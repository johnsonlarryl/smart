from pandas import DataFrame
from dataclasses import dataclass
from numbers import Real


@dataclass
class SmartGoal:
    column: str
    specific: str
    measurable: Real
    achievable: DataFrame
    realistic: DataFrame
    timely: Real
