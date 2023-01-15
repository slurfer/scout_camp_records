from constants import *
from abc import abstractmethod
from typing import Dict, Tuple, List, Any
from value import Value
from Errors import *
from database_table import DatabaseTable





TABLE = TAGS_DATABASE

class Tag(DatabaseTable):
    TABLE_NAME: str = TAGS_DATABASE


    def __init__(
        self,
        id: int = None,
        name: str = None,
        color: str = None,
        description: str = None,
        query: str = None
    ) -> None:
        # -------- values --------
        if not query == None:
            self.init_from_query(query)
        else:
            self.values: Dict[str, Value] = {
            ID: Value(ID, int, True, id, primary_key=True, editable=False),
            NAME: Value(NAME, str, True, name),
            COLOR: Value(COLOR, str, True, color),
            DESCRIPTION: Value(DESCRIPTION, str, True, description),
        }
    
    def init_from_query(self, query):
        id = int(query[0])
        name = str(query[1])
        color = str(query[2])
        description = str(query[3])
        self.values: Dict[str, Value] = {
            ID: Value(ID, int, True, id, primary_key=True, editable=False),
            NAME: Value(NAME, str, True, name),
            COLOR: Value(COLOR, str, False, color),
            DESCRIPTION: Value(DESCRIPTION, str, False, description),
        }
    

    def __dict__(self):
        return {
            ID: self.values[ID].value,
            NAME: self.values[NAME].value,
            COLOR: self.values[COLOR].value,
            DESCRIPTION: self.values[DESCRIPTION].value,
        }

        
        
        
    
    @staticmethod
    def generate_select_query() -> str:
        return f'SELECT * FROM {Tag.TABLE_NAME};'
    

            
    

        
    
    


