from constants import *
from abc import ABCMeta, abstractmethod
from typing import Dict, Tuple, List, Any
from value import Value
from Errors import *
import json
import copy


class DatabaseTable():
    RATING_MINIMAL_VALUE: int
    RAGING_MAXIMAL_VALUE: int
    TABLE_NAME: str
    VALUE_INFO: Dict[str, Value]
    FOREIGN_KEYS: List[Tuple[str, str]]

    def __init__(self) -> None:
        self.values: Dict[str, Value]


    def init_from_tuple(self, tuple: Tuple[Any], ignore_values_with_not_store_flag: bool = False):
        value_keys = list(self.VALUE_INFO.keys())
        i = 0
        self.values = {}
        skipped_values = 0
        while i < len(value_keys):
            value_name = value_keys[i]
            value_value = tuple[i-skipped_values]
            value_instance = copy.copy(self.VALUE_INFO[value_name])
            if self.VALUE_INFO[value_name].do_store or ignore_values_with_not_store_flag:
                value_instance.force_update(tuple[i-skipped_values])
            else:
                skipped_values += 1
            self.values[value_name] = value_instance
            i += 1
    
    def init_from_request(self, data: Dict[str, Any], id: int = None):
        data[ID] = id
        value_keys = list(self.VALUE_INFO.keys())
        provided_data_keys = list(data.keys())
        self.values = {}
        for key in value_keys:
            value_instance = copy.copy(self.VALUE_INFO[key])
            if key in provided_data_keys:
                value_instance.force_update(data[key], set_updated=True)
            else:
                value_instance.force_update(None)
            self.values[key] = value_instance

        
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
            if value.primary_key or not value.do_store:
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
            if value.primary_key or not value.do_store:
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
            value = self.values[value_name]
            if not value.is_metadata:
                output_dict[value_name] = value.value
        
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
    
    def __dict__(self):
        output_dict = {}
        for value_name in self.values.keys():
            value = self.values[value_name]
            if not value.is_metadata:
                output_dict[value_name] = value.value
        
        return output_dict
