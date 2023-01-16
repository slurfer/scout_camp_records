from constants import *
from abc import abstractmethod
from typing import Dict, Tuple, List, Any
from value import Value
from Errors import *
from database_table import DatabaseTable
import json





TABLE = PARENTS_DATABASE

class Parent(DatabaseTable):
    RATING_MINIMAL_VALUE: int = 0
    RAGING_MAXIMAL_VALUE: int = 5
    TABLE_NAME: str = PARENTS_DATABASE



    def __init__(
        self,
        id: int = None,
        name: str = None,
        surname: str = None,
        relationship_with_child: str = None,
        phone: int = None,
        email: str = None,
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
            RELATIONSHIP_WITH_CHILD: Value(RELATIONSHIP_WITH_CHILD, str, True, relationship_with_child),
            PHONE: Value(PHONE, str, False, phone),
            EMAIL: Value(EMAIL, str, False, email)
        }
    
    def init_from_query(self, query):
        id = int(query[0])
        name = str(query[1])
        surname = str(query[2])
        relationship_with_child = str(query[3])
        phone = str(query[4])
        email = str(query[5])
        self.values: Dict[str, Value] = {
            ID: Value(ID, int, True, id, primary_key=True, editable=False),
            NAME: Value(NAME, str, True, name),
            SURNAME: Value(SURNAME, str, True, surname),
            RELATIONSHIP_WITH_CHILD: Value(RELATIONSHIP_WITH_CHILD, str, True, relationship_with_child),
            PHONE: Value(PHONE, str, False, phone),
            EMAIL: Value(EMAIL, str, False, email)
        }
    

    def __dict__(self):
        return {
            ID: self.values[ID].value,
            NAME: self.values[NAME].value,
            SURNAME: self.values[SURNAME].value,
            RELATIONSHIP_WITH_CHILD: self.values[RELATIONSHIP_WITH_CHILD].value,
            PHONE: self.values[PHONE].value,
            EMAIL: self.values[EMAIL].value
        }

        
        
        
    
    @staticmethod
    def generate_select_query() -> str:
        return f'SELECT * FROM {Parent.TABLE_NAME};'
    

            
    

        
    
    


