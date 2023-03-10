from member import Member
from constants import *
from Errors import *
import pytest
from typing import Tuple, Any
from testing_database_table import MyTest
import datetime


instance1 = Member(id=96, name="Alfons", surname="Mucha", birth_date="2004-07-12", age_category_id=1, gender="muž", mother_id=1, father_id=2, description='Ahoj')
instance2 = Member(id=96, surname="Mucha", birth_date="2004-07-12", age_category_id=1, gender="muž", mother_id=1, father_id=2, description='Ahoj')
instance3 = Member(id=96, name="Alfons", birth_date="2004-07-12", age_category_id=1, gender="muž", mother_id=1, father_id=2, description='Ahoj')
instance4 = Member(id=96, name="Alfons", surname="Mucha", age_category_id=1, gender="muž", mother_id=1, father_id=2, description='Ahoj')
instance5 = Member(id=96, name="Alfons", surname="Mucha", birth_date="2004-07-12", age_category_id=1, mother_id=1, father_id=2, description='Ahoj')
instance6 = Member(id=96, name="Alfons", surname="Mucha", birth_date="2004-07-12", age_category_id=1, gender="muž", father_id=2, description='Ahoj')
instance7 = Member(id=96, name="Alfons", surname="Mucha", birth_date="2004-07-12", age_category_id=1, gender="muž", mother_id=1, father_id=2)
instance8 = Member(id=96, name="Alfons", surname="Mucha", birth_date="2004-07-12", gender="muž", mother_id=1, father_id=2)

# metadata
instance9 = Member(id=96, time_created='2022-09-04 12:34:56', name="Alfons", surname="Mucha", birth_date="2004-07-12", age_category_id=1, gender="muž", mother_id=1, father_id=2, description='Ahoj')
instance10 = Member(id=96, time_created='2022-09-04 12:34:56', time_updated='2022-09-05 15:16:24', name="Alfons", surname="Mucha", birth_date="2004-07-12", age_category_id=1, gender="muž", mother_id=1, father_id=2, description='Ahoj')

# not storing data
instance11 = Member(id=96, name="Alfons", surname="Mucha", birth_date="2004-07-12", age_category_id=1, gender="muž", mother_id=1, father_id=2, description='Ahoj')
# 
# query
instance1_query = (96, datetime.date(2004, 7, 12), datetime.date(2004, 7, 12), 'Alfons', 'Mucha', datetime.date(2004, 7, 12), 1, 'muž', 1, 2, 'Ahoj')
instance5_query = ((12, 'Alfons', 'Mucha', datetime.date(2004, 7, 12), 1, None, 1, 2, 'Ahoj'))
instance6_query = ((13, 'Alfons', 'Mucha', datetime.date(2004, 7, 12), 1, 'muž', None, 2, 'Ahoj'))
instance7_query = ((14, 'Alfons', 'Mucha', datetime.date(2004, 7, 12), 1, 'muž', 1, 2, None))
instance8_query = ()
instance9_query = ()
instance10_query = ()
instance11_query = ((96, datetime.date(2004, 7, 12), datetime.date(2004, 7, 12), 'Alfons', 'Mucha', datetime.date(2004, 7, 12), 1, 'muž', 1, 2, 'Ahoj'))


# -------- testing create instance --------
MyTest.create_instance_from_query(instance1_query, Member, instance1)
MyTest.create_instance_from_query(instance11_query, Member, instance11)

# -------- testing create instance from request --------
request_data = {'name': 'Martin', 'surname': 'Doušek', 'birth_date': '2004-09-17', 'description': 'So this is good.', 'age_category_id': 1, 'mother_id': 1, 'father_id': 2, 'camp_ids': [1, 2, 3]}
request_intance = Member(name='Martin', surname='Doušek', birth_date='2004-09-17', description='So this is good.', age_category_id=1, mother_id=1, father_id=2, camp_ids=[1, 2, 3])
MyTest.test_create_instance_from_request(request_data, class_variable=Member, instance=request_intance)

# -------- testing get --------
MyTest.test_select_query(Member, 'SELECT * FROM members;')


# -------- testing post --------
MyTest.test_create_insert_query(instance1, sql_string=('INSERT INTO members (name, surname, birth_date, age_category_id, gender, mother_id, father_id, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', ['Alfons', 'Mucha', '2004-07-12', 1, 'muž', 1, 2, 'Ahoj']))
MyTest.test_create_insert_query(instance2, value_name=NAME)
MyTest.test_create_insert_query(instance3, value_name=SURNAME)
MyTest.test_create_insert_query(instance4, value_name=BIRTH_DATE)
MyTest.test_create_insert_query(instance5, sql_string=('INSERT INTO members (name, surname, birth_date, age_category_id, mother_id, father_id, description) VALUES (%s, %s, %s, %s, %s, %s, %s)', ['Alfons', 'Mucha', '2004-07-12', 1, 1, 2, 'Ahoj']))
MyTest.test_create_insert_query(instance6, sql_string=('INSERT INTO members (name, surname, birth_date, age_category_id, gender, father_id, description) VALUES (%s, %s, %s, %s, %s, %s, %s)', ['Alfons', 'Mucha', '2004-07-12', 1, 'muž', 2, 'Ahoj']))
MyTest.test_create_insert_query(instance7, sql_string=('INSERT INTO members (name, surname, birth_date, age_category_id, gender, mother_id, father_id) VALUES (%s, %s, %s, %s, %s, %s, %s)', ['Alfons', 'Mucha', '2004-07-12', 1, 'muž', 1, 2]))
MyTest.test_create_insert_query(instance8, sql_string=('INSERT INTO members (name, surname, birth_date, gender, mother_id, father_id) VALUES (%s, %s, %s, %s, %s, %s)', ['Alfons', 'Mucha', '2004-07-12', 'muž', 1, 2]))
MyTest.test_create_insert_query(instance9, sql_string=('INSERT INTO members (time_created, name, surname, birth_date, age_category_id, gender, mother_id, father_id, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', ['2022-09-04 12:34:56', 'Alfons', 'Mucha', '2004-07-12', 1, 'muž', 1, 2, 'Ahoj']))
MyTest.test_create_insert_query(instance10, sql_string=('INSERT INTO members (time_created, time_updated, name, surname, birth_date, age_category_id, gender, mother_id, father_id, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', ['2022-09-04 12:34:56', '2022-09-05 15:16:24', 'Alfons', 'Mucha', '2004-07-12', 1, 'muž', 1, 2, 'Ahoj']))
MyTest.test_create_insert_query(instance11, sql_string=('INSERT INTO members (name, surname, birth_date, age_category_id, gender, mother_id, father_id, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', ['Alfons', 'Mucha', '2004-07-12', 1, 'muž', 1, 2, 'Ahoj']))


# -------- testing put --------
MyTest.test_create_update_query(instance1, empty_update=True)
MyTest.test_create_update_query(instance1, NAME, 'Božena', sql_string=('UPDATE members SET name = %s WHERE id = %s', ['Božena', 96]))
MyTest.test_create_update_query(instance1, SURNAME, 'Němcová', sql_string=('UPDATE members SET surname = %s WHERE id = %s', ['Němcová', 96]))
MyTest.test_create_update_query(instance1, BIRTH_DATE, '1820-02-04', sql_string=('UPDATE members SET birth_date = %s WHERE id = %s', ['1820-02-04', 96]))
MyTest.test_create_update_query(instance1, AGE_CATEGORY_ID, 10, sql_string=('UPDATE members SET age_category_id = %s WHERE id = %s', [10, 96]))
MyTest.test_create_update_query(instance1, GENDER, 'žena', sql_string=('UPDATE members SET gender = %s WHERE id = %s', ['žena', 96]))
MyTest.test_create_update_query(instance1, MOTHER_ID, 5, sql_string=('UPDATE members SET mother_id = %s WHERE id = %s', [5, 96]))
MyTest.test_create_update_query(instance1, FATHER_ID, 6, sql_string=('UPDATE members SET father_id = %s WHERE id = %s', [6, 96]))
MyTest.test_create_update_query(instance1, DESCRIPTION, 'Babička', sql_string=('UPDATE members SET description = %s WHERE id = %s', ['Babička', 96]))


# -------- testing delete --------
assert instance1.generate_delete_query() == ('DELETE FROM members WHERE id = %s;', [96]), f'problem during testing delete query:\n{instance1.generate_delete_query()}'


# -------- test record to str --------
MyTest.test_instance_to_string(instance1, '{"id": 96, "name": "Božena", "surname": "Němcová", "birth_date": "1820-02-04", "age_category_id": 10, "gender": "žena", "mother_id": 5, "father_id": 6, "camp_ids": null, "description": "Babička"}')
MyTest.test_instance_to_string(instance2, '{"id": 96, "name": null, "surname": "Mucha", "birth_date": "2004-07-12", "age_category_id": 1, "gender": "muž", "mother_id": 1, "father_id": 2, "camp_ids": null, "description": "Ahoj"}')
MyTest.test_instance_to_string(instance3, '{"id": 96, "name": "Alfons", "surname": null, "birth_date": "2004-07-12", "age_category_id": 1, "gender": "muž", "mother_id": 1, "father_id": 2, "camp_ids": null, "description": "Ahoj"}')
MyTest.test_instance_to_string(instance4, '{"id": 96, "name": "Alfons", "surname": "Mucha", "birth_date": null, "age_category_id": 1, "gender": "muž", "mother_id": 1, "father_id": 2, "camp_ids": null, "description": "Ahoj"}')
MyTest.test_instance_to_string(instance5, '{"id": 96, "name": "Alfons", "surname": "Mucha", "birth_date": "2004-07-12", "age_category_id": 1, "gender": null, "mother_id": 1, "father_id": 2, "camp_ids": null, "description": "Ahoj"}')
MyTest.test_instance_to_string(instance6, '{"id": 96, "name": "Alfons", "surname": "Mucha", "birth_date": "2004-07-12", "age_category_id": 1, "gender": "muž", "mother_id": null, "father_id": 2, "camp_ids": null, "description": "Ahoj"}')
MyTest.test_instance_to_string(instance7, '{"id": 96, "name": "Alfons", "surname": "Mucha", "birth_date": "2004-07-12", "age_category_id": 1, "gender": "muž", "mother_id": 1, "father_id": 2, "camp_ids": null, "description": null}')
MyTest.test_instance_to_string(instance9, '{"id": 96, "name": "Alfons", "surname": "Mucha", "birth_date": "2004-07-12", "age_category_id": 1, "gender": "muž", "mother_id": 1, "father_id": 2, "camp_ids": null, "description": "Ahoj"}')
MyTest.test_instance_to_string(instance10, '{"id": 96, "name": "Alfons", "surname": "Mucha", "birth_date": "2004-07-12", "age_category_id": 1, "gender": "muž", "mother_id": 1, "father_id": 2, "camp_ids": null, "description": "Ahoj"}')

# -------- test record to json --------
MyTest.test_instance_to_dict(instance1, {"id": 96, "name": "Božena", "surname": "Němcová", "birth_date": "1820-02-04", "age_category_id": 10, "gender": "žena", "mother_id": 5, "father_id": 6, "camp_ids": None, "description": "Babička"})
MyTest.test_instance_to_dict(instance2, {"id": 96, "name": None, "surname": "Mucha", "birth_date": "2004-07-12", "age_category_id": 1, "gender": "muž", "mother_id": 1, "father_id": 2, "camp_ids": None, "description": "Ahoj"})
MyTest.test_instance_to_dict(instance3, {"id": 96, "name": "Alfons", "surname": None, "birth_date": "2004-07-12", "age_category_id": 1, "gender": "muž", "mother_id": 1, "father_id": 2, "camp_ids": None, "description": "Ahoj"})
MyTest.test_instance_to_dict(instance4, {"id": 96, "name": "Alfons", "surname": "Mucha", "birth_date": None, "age_category_id": 1, "gender": "muž", "mother_id": 1, "father_id": 2, "camp_ids": None, "description": "Ahoj"})
MyTest.test_instance_to_dict(instance5, {"id": 96, "name": "Alfons", "surname": "Mucha", "birth_date": "2004-07-12", "age_category_id": 1, "gender": None, "mother_id": 1, "father_id": 2, "camp_ids": None, "description": "Ahoj"})
MyTest.test_instance_to_dict(instance6, {"id": 96, "name": "Alfons", "surname": "Mucha", "birth_date": "2004-07-12", "age_category_id": 1, "gender": "muž", "mother_id": None, "father_id": 2, "camp_ids": None, "description": "Ahoj"})
MyTest.test_instance_to_dict(instance7, {"id": 96, "name": "Alfons", "surname": "Mucha", "birth_date": "2004-07-12", "age_category_id": 1, "gender": "muž", "mother_id": 1, "father_id": 2, "camp_ids": None, "description": None})
MyTest.test_instance_to_dict(instance9, {"id": 96, "name": "Alfons", "surname": "Mucha", "birth_date": "2004-07-12", "age_category_id": 1, "gender": "muž", "mother_id": 1, "father_id": 2, "camp_ids": None, "description": "Ahoj"})
MyTest.test_instance_to_dict(instance10, {"id": 96, "name": "Alfons", "surname": "Mucha", "birth_date": "2004-07-12", "age_category_id": 1, "gender": "muž", "mother_id": 1, "father_id": 2, "camp_ids": None, "description": "Ahoj"})
MyTest.test_instance_to_dict(instance11, {"id": 96, "name": "Alfons", "surname": "Mucha", "birth_date": "2004-07-12", "age_category_id": 1, "gender": "muž", "mother_id": 1, "father_id": 2, "camp_ids": None, "description": "Ahoj"})

# -------- test if all obligatory arguments passed --------
MyTest.test_check_if_all_obligatory_values_provided(instance2, NAME, True)
MyTest.test_check_if_all_obligatory_values_provided(instance3, SURNAME, True)
MyTest.test_check_if_all_obligatory_values_provided(instance4, BIRTH_DATE, True)
MyTest.test_check_if_all_obligatory_values_provided(instance8, AGE_CATEGORY_ID, False)
MyTest.test_check_if_all_obligatory_values_provided(instance5, GENDER, False)
MyTest.test_check_if_all_obligatory_values_provided(instance5, MOTHER_ID, False)
MyTest.test_check_if_all_obligatory_values_provided(instance6, FATHER_ID, False)
MyTest.test_check_if_all_obligatory_values_provided(instance7, DESCRIPTION, False)

