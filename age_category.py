from constants import *
from abc import abstractmethod
from typing import Dict, Tuple, List, Any
from value import Value
from Errors import *
from database_table import DatabaseTable
import json





TABLE = AGE_CATEGORIES_DATABASE

class AgeCategory(DatabaseTable):
    RATING_MINIMAL_VALUE: int = 0
    RAGING_MAXIMAL_VALUE: int = 5
    TABLE_NAME: str = AGE_CATEGORIES_DATABASE
    VALUE_INFO: Dict[str, Value] = {
            ID: Value(ID, int, True, primary_key=True, editable=False),
            NAME: Value(NAME, str, True),
        }
    FOREIGN_KEYS: List[Tuple[str, str]] = None



    def __init__(
        self,
        id: int = None,
        name: str = None,
        query: str = None,
        request: Dict[str, Any] = None
    ) -> None:
        # -------- values --------
        if not query == None:
            self.init_from_tuple(query)
        elif not request == None:
            self.init_from_request(request, id)
        else:
            self.init_from_tuple((
                id,
                name
            ))
    
    @staticmethod
    def generate_select_query() -> str:
        return f'SELECT * FROM {AgeCategory.TABLE_NAME};'
    

            
    

        
    
    


