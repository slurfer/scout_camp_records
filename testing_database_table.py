from constants import *
from Errors import *
import pytest
from typing import Tuple, Any


# ========================== FUNCTIONS ==========================
class MyTest:
    def test_select_query(class_variable, sql_string):
        returned_sql_string = class_variable.generate_select_query()
        assert returned_sql_string == sql_string, f'Wrong return during testing SELECT query:\n{returned_sql_string}\nreturned instead of:\n{sql_string}'

    def test_create_insert_query(instance, value_name: str = None, sql_string: Tuple = None):
        if not sql_string==None:
            returned_sql_string = instance.generate_insert_query()
            assert returned_sql_string == sql_string, f'Wrong return during testing INSERT query:\n{returned_sql_string}\nreturned instead of:\n{sql_string}'
        else:
            try:
                instance.generate_insert_query()
            except MissingOblitagoryValue as error:
                assert error.value_name==value_name, f"Value Error: \n{error.value_name}"

    def test_create_update_query(instance, value_name: str = None, new_value: Any = None, sql_string: Tuple = None, empty_update = False):
        if empty_update:
            try:
                instance.generate_update_query()
            except EmptyRequest as error:
                assert str(error)=='Empty Request', f'Wrong return during testing UPDATE query:\nEmpty Request not empty'
        else:
            instance.update_value(value_name, new_value)
            returned_sql_string = instance.generate_update_query()
            assert returned_sql_string == sql_string, f'Wrong return during testing UPDATE query:\n{returned_sql_string}\nreturned instead of:\n{sql_string}'

    def test_instance_to_string(instance, final_string: str):
        assert str(instance) == final_string, f'Error in converting record to string. Function returned:\n{str(instance)}\nreturned instead of:\n{final_string}'
    
    def test_instance_to_dict(instance, final_dict: str):
        assert instance.__dict__() == final_dict, f'Error in converting record to json. Function returned:\n{str(instance)}\nreturned instead of:\n{final_dict}'

    def test_check_if_all_obligatory_values_provided(instance, value_name: str, is_obligatory: bool):
        if is_obligatory:
            try:
                instance.check_if_all_obligatory_values_provided()
            except MissingOblitagoryValue as error:
                assert error.value_name==value_name, f"Value Error: \n{error.value_name}"
        else:
            assert instance.check_if_all_obligatory_values_provided()==True, f"Value Error: \n{instance.check_if_all_obligatory_values_provided()}"
    
    def create_instance_from_query(query: Tuple, class_variable, instance):
        new_instance = class_variable(query=query)
        assert str(new_instance) == str(instance), f'Error in extracting record from query. Function returned:\n{str(new_instance)}\nreturned instead of:\n{str(instance)}'
    
    def test_create_instance_from_request(data: Dict[str, Any], class_variable, instance, id: int=None, instance2=None):
        new_instance = class_variable(request=data)
        assert str(new_instance) == str(instance), f'Error in extracting record from response. Function returned:\n{str(new_instance)}\nreturned instead of:\n{str(instance)}'
        if not id==None:
            new_instance2 = class_variable(request=data, id=id)
            assert str(new_instance2) == str(instance2), f'Error in extracting record from response with id. Function returned:\n{str(new_instance)}\nreturned instead of:\n{str(instance)}'
