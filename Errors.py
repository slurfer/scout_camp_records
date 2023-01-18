from typing import Dict, Tuple, List, Any
import json

class MissingOblitagoryValue(Exception):
    def __init__(self, value_name = '') -> None:
        self.value_name = value_name
    
    def __str__(self) -> str:
        return f'Missing obligatory value "{self.value_name}"'

class TryingToUpdateUnupdatableValue(Exception):
    def __init__(self, value_name: str) -> None:
        self.message = f'Trying tu update to unupdatable value "{self.value_name}"'
        self.code = 400
    
    def __str__(self) -> str:
        return self.message

class FailedToConnnectToDatabase(Exception):
    pass


class NonExistingKey(Exception):
    def __init__(self, key_name, key_value) -> None:
        self.message = f'Non existing key ({key_name} with value {key_value})'

    def __str__(self) -> str:
        return self.message


class EmptyRequest(Exception):
    def __init__(self) -> None:
        self.message = f'Empty Request'

    def __str__(self) -> str:
        return self.message



class DatabaseOperationResult:
    def __init__(self, message: str = 'Successful operation', code: int = 200, data: Any = None) -> None:
        self.message = message
        self.code = 400
        self.data = data
    
    def __str__(self):
        return self.message