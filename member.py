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
        name: str = None,
        surname: str = None,
        birth_date: str = None,
        age_category_id: int = None,
        gender: str = None,
        mother_id = None,
        father_id: List[int] = None,
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
            SURNAME: Value(SURNAME, str, True, surname),
            BIRTH_DATE: Value(BIRTH_DATE, str, True, birth_date),
            AGE_CATEGORY_ID: Value(AGE_CATEGORY_ID, int, False, age_category_id),
            GENDER: Value(GENDER, str, False, gender),
            MOTHER_ID: Value(MOTHER_ID, int, False, mother_id),
            FATHER_ID: Value(FATHER_ID, int, False, father_id),
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
    

    def __dict__(self):
        return {
            ID: self.values[ID].value,
            NAME: self.values[NAME].value,
            SURNAME: self.values[SURNAME].value,
            BIRTH_DATE: self.values[BIRTH_DATE].value,
            AGE_CATEGORY_ID: self.values[AGE_CATEGORY_ID].value,
            GENDER: self.values[GENDER].value,
            MOTHER_ID: self.values[MOTHER_ID].value,
            FATHER_ID: self.values[FATHER_ID].value,
            DESCRIPTION: self.values[DESCRIPTION].value,
        }

        
        
        
    
    @staticmethod
    def generate_select_query() -> str:
        return f'SELECT * FROM {Member.TABLE_NAME};'
    

            
    

        
    
    


