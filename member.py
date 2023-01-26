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
    VALUE_INFO: Dict[str, Value] = {
        ID: Value(ID, int, True, primary_key=True, editable=False),
        TIME_CREATED: Value(TIME_CREATED, str, False, is_metadata=True),
        TIME_UPDATED: Value(TIME_UPDATED, str, False, is_metadata=True),
        NAME: Value(NAME, str, True),
        SURNAME: Value(SURNAME, str, True),
        BIRTH_DATE: Value(BIRTH_DATE, str, True),
        AGE_CATEGORY_ID: Value(AGE_CATEGORY_ID, int, False),
        GENDER: Value(GENDER, str, False),
        MOTHER_ID: Value(MOTHER_ID, int, False),
        FATHER_ID: Value(FATHER_ID, int, False),
        CAMP_IDS: Value(CAMP_IDS, list, False, do_store=False),
        DESCRIPTION: Value(DESCRIPTION, str, False)
    }
    FOREIGN_KEYS: List[Tuple[str, str]] = [
        (AGE_CATEGORY_ID, AGE_CATEGORIES_DATABASE),
        (MOTHER_ID, PARENTS_DATABASE),
        (FATHER_ID, PARENTS_DATABASE),
    ]



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
                time_created,
                time_updated,
                name,
                surname,
                birth_date,
                age_category_id,
                gender,
                mother_id,
                father_id,
                camp_ids,
                description
            ), ignore_values_with_not_store_flag=True)
    @staticmethod
    def generate_select_query() -> str:
        return f'SELECT * FROM {Member.TABLE_NAME};'
    

            
    

        
    
    


