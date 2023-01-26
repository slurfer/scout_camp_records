from constants import *
from abc import abstractmethod
from typing import Dict, Tuple, List, Any
from value import Value
from Errors import *
from database_table import DatabaseTable
import json





TABLE = PARTICIPANTS_DATABASE

class Participant(DatabaseTable):
    RATING_MINIMAL_VALUE: int = 0
    RAGING_MAXIMAL_VALUE: int = 5
    TABLE_NAME: str = PARTICIPANTS_DATABASE
    VALUE_INFO: Dict[str, Value] = {
            ID: Value(ID, int, True, primary_key=True, editable=False),
            MEMBER_ID: Value(NAME, int, True),
            CAMP_ID: Value(SURNAME, int, True),
        }
    FOREIGN_KEYS: List[Tuple[str, str]] = None



    def __init__(
        self,
        id: int = None,
        member_id: int = None,
        camp_id: int = None,
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
                member_id,
                camp_id
            ))
    
    def generate_get_all_camps_query(self):
        return 'SELECT camp_id FROM participants where member_id=%s;', [self.values[MEMBER_ID].value]
    
    @staticmethod
    def generate_select_query() -> str:
        return f'SELECT * FROM {Participant.TABLE_NAME};'
    

            
    

        
    
    


