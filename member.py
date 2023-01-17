from constants import *
from abc import abstractmethod
from typing import Dict, Tuple, List, Any
from value import Value
from Errors import *
from database_table import DatabaseTable
import json





TABLE = MEMBERS_DATABASE

class Member(DatabaseTable):
    TABLE_NAME: str = MEMBERS_DATABASE



    def __init__(
        self,
        id: int = None,
        time_created: str = None,
        time_updated: str = None,
        name: str = None,
        surname: str = None,
        birth_date: str = None,
        age_category_id: int = None,
        gender: str = None,
        mother_id = None,
        father_id: int = None,
        camp_ids: List[int] = None,
        description: str = None,
        query: str = None
    ) -> None:
        # -------- values --------
        if not query == None:
            self.init_from_query(query)
        else:
            self.values: Dict[str, Value] = {
            ID: Value(ID, int, True, id, primary_key=True, editable=False),
            TIME_CREATED: Value(TIME_CREATED, str, False, time_created, is_metadata=True),
            TIME_UPDATED: Value(TIME_UPDATED, str, False, time_updated, is_metadata=True),
            NAME: Value(NAME, str, True, name),
            SURNAME: Value(SURNAME, str, True, surname),
            BIRTH_DATE: Value(BIRTH_DATE, str, True, birth_date),
            AGE_CATEGORY_ID: Value(AGE_CATEGORY_ID, int, False, age_category_id),
            GENDER: Value(GENDER, str, False, gender),
            MOTHER_ID: Value(MOTHER_ID, int, False, mother_id),
            FATHER_ID: Value(FATHER_ID, int, False, father_id),
            # CAMP_IDS: Value(CAMP_IDS, List[int], False, camp_ids, do_store=False),
            DESCRIPTION: Value(DESCRIPTION, str, False, description)
        }
    
    def init_from_query(self, query):
        id = int(query[0])
        name = str(query[1])
        surname = str(query[2])
        birth_date = str(query[3])
        age_category_id = str(query[4])
        gender = str(query[5])
        mother_id = str(query[6])
        father_id = str(query[7])
        description = str(query[8])
        self.values: Dict[str, Value] = {
            ID: Value(ID, int, True, id, primary_key=True, editable=False),
            NAME: Value(NAME, str, True, name),
            SURNAME: Value(SURNAME, str, True, surname),
            BIRTH_DATE: Value(BIRTH_DATE, str, True, birth_date),
            AGE_CATEGORY_ID: Value(AGE_CATEGORY_ID, int, False, age_category_id),
            GENDER: Value(GENDER, str, False, gender),
            MOTHER_ID: Value(MOTHER_ID, int, False, mother_id),
            FATHER_ID: Value(FATHER_ID, int, False, father_id),
            DESCRIPTION: Value(DESCRIPTION, str, False, description)
        }
    


        
        
        
    
    @staticmethod
    def generate_select_query() -> str:
        return f'SELECT * FROM {Member.TABLE_NAME};'
    

            
    

        
    
    


