from typing import Dict, Tuple, List, Any
from record import Record
import json

class SelectQueryResponse:
    def __init__(self, data: List[Any]) -> None:
        self.data = data


class Query:
    def __init__(self, data) -> None:
        self.data = data