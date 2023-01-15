from dataclasses import dataclass
from typing import Any
from Errors import *

@dataclass
class Value:
    def __init__(
        self,
        name: str,
        type: Any,
        is_obligatory: bool,
        value = None,
        not_provided_error_statement: str = 'Value not provided',
        primary_key: bool = False,
        updated: bool = False,
        editable: bool = True
    ) -> None:
        self.name: str = name
        self.type: Any = type
        self.is_obligatory: bool = is_obligatory
        self._value = value
        self.not_provided_error_statement: str = not_provided_error_statement
        self.primary_key: bool = primary_key
        self.updated: bool = updated
        self.editable: bool = editable

    # -------- set property - value --------
    @property
    def value(self) -> Any:
        return self._value
    
    @value.setter
    def value(self, value: Any) -> None:
        if self.editable:
            self._value = value
        else:
            raise TryingToUpdateUnupdatableValue(self.name)
        self.updated = True


# instance1 = Value('Test', str, True, 'value')
# print(instance1.value, instance1.updated)
# instance1.value = 'zmena'
# print(instance1.value, instance1.updated)
