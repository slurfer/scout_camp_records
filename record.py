from constants import *
from abc import abstractmethod
from typing import Dict, Tuple, List, Any
from value import Value
from Errors import *
from database_table import DatabaseTable
import json





TABLE = 'records'

class Record(DatabaseTable):
    RATING_MINIMAL_VALUE: int = 0
    RAGING_MAXIMAL_VALUE: int = 5
    TABLE_NAME: str = 'records'



    def __init__(
        self,
        id: int = None,
        datetime: str = None,
        programming_language: str = None,
        minutes_spent: int = None,
        rating: int = None,
        programmer_id: int = None,
        description = None,
        tag_ids: List[int] = None,
        query: str = None
    ) -> None:
        # -------- values --------
        if not query == None:
            self.init_from_query(query)
        else:
            self.values: Dict[str, Value] = {
            ID: Value(ID, int, True, id, primary_key=True, editable=False),
            DATETIME: Value(DATETIME, str, True, datetime),
            PROGRAMMING_LANGUAGE: Value(PROGRAMMING_LANGUAGE, str, True, programming_language),
            MINUTES_SPENT: Value(MINUTES_SPENT, int, True, minutes_spent),
            RATING: Value(RATING, int, True, rating),
            PROGRAMMER_ID: Value(PROGRAMMER_ID, int, False, programmer_id),
            TAG_IDS: Value(TAG_IDS, str, False, tag_ids),
            DESCRIPTION: Value(DESCRIPTION, str, False, description)
        }
    
    def init_from_query(self, query):
        id = int(query[0])
        datetime = str(query[3])
        programming_language = str(query[4])
        minutes_spent = int(query[5])
        rating = int(query[6])
        programmer_id = query[7]
        if not query[8] == None:
            tag_ids = json.loads(query[8])
        else:
            tag_ids = None
        description = query[9]
        self.values: Dict[str, Value] = {
            ID: Value(ID, int, True, id, primary_key=True, editable=False),
            DATETIME: Value(DATETIME, str, True, datetime),
            PROGRAMMING_LANGUAGE: Value(PROGRAMMING_LANGUAGE, str, True, programming_language),
            MINUTES_SPENT: Value(MINUTES_SPENT, int, True, minutes_spent),
            RATING: Value(RATING, int, True, rating),
            PROGRAMMER_ID: Value(PROGRAMMER_ID, int, False, programmer_id),
            TAG_IDS: Value(TAG_IDS, List[int], False, tag_ids),
            DESCRIPTION: Value(DESCRIPTION, str, False, description)
        }
    

    def __dict__(self):
        return {
            ID: self.values[ID].value,
            DATETIME: self.values[DATETIME].value,
            PROGRAMMING_LANGUAGE: self.values[PROGRAMMING_LANGUAGE].value,
            MINUTES_SPENT: self.values[MINUTES_SPENT].value,
            RATING: self.values[RATING].value,
            PROGRAMMER_ID: self.values[PROGRAMMER_ID].value,
            TAG_IDS: self.values[TAG_IDS].value,
            DESCRIPTION: self.values[DESCRIPTION].value,
        }

        
        
        
    
    @staticmethod
    def generate_select_query() -> str:
        return f'SELECT * FROM {Record.TABLE_NAME};'
    

            
    

        
    
    


