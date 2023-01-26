from constants import *
from abc import abstractmethod
from typing import Dict, Tuple, List, Any
from value import Value
from Errors import *
from database_table import DatabaseTable
import json





TABLE = CAMPS_DATABASE

class Camp(DatabaseTable):
    RATING_MINIMAL_VALUE: int = 0
    RAGING_MAXIMAL_VALUE: int = 5
    TABLE_NAME: str = CAMPS_DATABASE
    VALUE_INFO: Dict[str, Value] = {
            ID: Value(ID, int, True, primary_key=True, editable=False),
            STARTS_ON: Value(STARTS_ON, str, True),
            ENDS_ON: Value(ENDS_ON, str, True),
            LEADER_ID: Value(LEADER_ID, int, True),
            LEADER_DEPUTY_ID: Value(LEADER_DEPUTY_ID, int, False),
            MEDIC_ID: Value(MEDIC_ID, int, False)
        }
    FOREIGN_KEYS: List[Tuple[str, str]] = [
        (LEADER_ID, MEMBERS_DATABASE),
        (LEADER_DEPUTY_ID, MEMBERS_DATABASE),
        (MEDIC_ID, MEMBERS_DATABASE),
    ]



    def __init__(
        self,
        id: int = None,
        starts_on: str = None,
        ends_on: str = None,
        leader_id: int = None,
        leader_deputy_id: int = None,
        medic: int = None,
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
                starts_on,
                ends_on,
                leader_id,
                leader_deputy_id,
                medic
            ))
    
    @staticmethod
    def generate_select_query() -> str:
        return f'SELECT * FROM {Camp.TABLE_NAME};'
    

            
    

        
    
    


