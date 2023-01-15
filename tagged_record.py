from constants import *
from abc import abstractmethod
from typing import Dict, Tuple, List, Any
from value import Value
from Errors import *
from database_table import DatabaseTable





TABLE = TAGGED_RECORDS_DATABASE

class TaggedRecord(DatabaseTable):
    TABLE_NAME: str = TAGGED_RECORDS_DATABASE


    def __init__(
        self,
        id: int = None,
        record_id: int = None,
        tag_id: int = None,
        query: str = None
    ) -> None:
        # -------- values --------
        if not query == None:
            self.init_from_query(query)
        else:
            self.values: Dict[str, Value] = {
            ID: Value(ID, int, True, id, primary_key=True, editable=False),
            RECORD_ID: Value(NAME, int, True, record_id),
            TAG_ID: Value(COLOR, int, True, tag_id),
        }
    
    def init_from_query(self, query):
        print(query)
        id = int(query[0])
        record_id = int(query[1])
        tag_id = int(query[2])
        self.values: Dict[str, Value] = {
            ID: Value(ID, int, True, id, primary_key=True, editable=False),
            RECORD_ID: Value(NAME, int, True, record_id),
            TAG_ID: Value(COLOR, int, True, tag_id),
        }
    

    def __dict__(self):
        return {
            ID: self.values[ID].value,
            RECORD_ID: self.values[RECORD_ID].value,
            TAG_ID: self.values[TAG_ID].value,
        }

        
        
        
    
    @staticmethod
    def generate_select_query() -> str:
        return f'SELECT * FROM {TaggedRecord.TABLE_NAME};'
    

            
    

        
    
    


