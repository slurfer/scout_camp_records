from constants import *
from abc import ABCMeta, abstractmethod
from typing import Dict, Tuple, List, Any
from value import Value
from Errors import *
import json


class DatabaseTable():
    RATING_MINIMAL_VALUE: int
    RAGING_MAXIMAL_VALUE: int
    TABLE_NAME: str

    def __init__(self) -> None:
        self.values: Dict[str, Value]


    def __get_data_from_query(self, query):
            pass
    
    def get_value_by_name(self, name: str) -> Value:
        for value in self.values:
            if value.name == name:
                return value

    def generate_select_query() -> str:
        return f'SELECT * FROM {DatabaseTable.TABLE_NAME};'
    
    def generate_insert_query(self) -> Tuple[str, List[Any]]:
        sql_header = f'INSERT INTO {self.TABLE_NAME} '
        sql_values = []
        columns = '('
        values_template = '('


        for value_name in self.values.keys():
            value = self.values[value_name]
            if value.primary_key:
                continue

            if not value.value == None:
                columns += value_name + ', '
                values_template += '%s, '
                if type(value.value) == list:
                    sql_values.append(json.dumps(value.value))
                else:
                    sql_values.append(value.value)
            elif value.is_obligatory:
                raise MissingOblitagoryValue(value_name)
        
        columns = columns[:-2] + ')'
        values_template = values_template[:-2] + ')'
        
        sql = sql_header + columns + ' VALUES ' + values_template
        return sql, sql_values

    def generate_update_query(self):
        sql_header = f'UPDATE {self.TABLE_NAME} SET'
        sql_values = []


        for value_name in self.values.keys():
            value = self.values[value_name]
            if value.primary_key:
                continue

            if value.updated:
                value.updated=False
                sql_header += ' ' + value_name + ' = %s, '
                if type(value.value) == list:
                    sql_values.append(json.dumps(value.value))
                else:
                    sql_values.append(value.value)
        
        if len(sql_values) == 0:
            raise EmptyRequest
        sql_values.append(self.values[ID].value)
        sql = sql_header[:-2] + f' WHERE id = %s'

        
        
        return sql, sql_values



    def generate_delete_query(self):
        return f'DELETE FROM {self.TABLE_NAME} WHERE id = %s;', [self.values[ID].value]

    def __str__(self) -> str:
        output_dict = {}
        for value_name in self.values.keys():
            output_dict[value_name] = self.values[value_name].value
        
        return json.dumps(output_dict, ensure_ascii=False)
    
    def update_value(self, property_name: str, updated_value_value):
        self.values[property_name].value = updated_value_value
        self.values[property_name].updated = True
    
    def check_if_all_obligatory_values_provided(self):
        for value_name in self.values.keys():
            value = self.values[value_name]
            if value.is_obligatory and value.value == None:
                raise MissingOblitagoryValue(value_name)
        return True
