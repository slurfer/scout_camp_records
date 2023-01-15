from constants import *
from abc import abstractmethod
from typing import Dict, Tuple, List, Any
from value import Value
from Errors import *
from database_table import DatabaseTable





TABLE = 'programmers'

class Programmer(DatabaseTable):
    TABLE_NAME: str = 'programmers'


    def __init__(
        self,
        id: int = None,
        name: str = None,
        surname: str = None,
        query: str = None
    ) -> None:
        # -------- values --------
        if not query == None:
            self.init_from_query(query)
        else:
            self.values: Dict[str, Value] = {
            ID: Value(ID, int, True, id, primary_key=True, editable=False),
            NAME: Value(NAME, str, True, name),
            SURNAME: Value(SURNAME, str, True, surname),
        }
    
    def init_from_query(self, query):
        id = int(query[0])
        name = str(query[1])
        surname = str(query[2])
        self.values: Dict[str, Value] = {
            ID: Value(ID, int, True, id, primary_key=True, editable=False),
            NAME: Value(NAME, str, True, name),
            SURNAME: Value(SURNAME, str, True, surname),
        }
    

    def __dict__(self):
        return {
            ID: self.values[ID].value,
            NAME: self.values[NAME].value,
            SURNAME: self.values[SURNAME].value,
        }

        
        
        
    
    @staticmethod
    def generate_select_query() -> str:
        return f'SELECT * FROM {Programmer.TABLE_NAME};'
    

            
    

        
    
    


