from datetime import datetime
from flask import Flask, request, abort, Request, jsonify
import flask
import json
from typing import Dict, Tuple, List, Any
from flask_cors import CORS
from member import Member
from parent import Parent
from constants import *
from tour_de_app_database import TourDeAppDatabase
from classes import *
from Errors import *

DATABASE = TourDeAppDatabase()


app = Flask("My first server")
CORS(app)


# ========================== TOOLS ==========================
def get_data_from_request(request: Request) -> Dict[str, Any]:
    if isinstance(request.json, str):
        data: Dict[str, str] = json.loads(request.json)
    else:
        data: Dict[str, str] = request.json
    
    return data


# ========================== MEMBERS ==========================

def create_member_instance(data: Dict[str, Any], member_id: int = None) -> Member:
    if not member_id == None:
        member = Member(
            id=member_id,
        )
    else:
        member = Member()

    # check, if obligatory values provided
    if NAME in data.keys():
        name = data[NAME]
        member.update_value(NAME, name)
    
    if SURNAME in data.keys():
        surname = data[SURNAME]
        member.update_value(SURNAME, surname)
    
    if BIRTH_DATE in data.keys():
        birth_date = data[BIRTH_DATE]
        member.update_value(BIRTH_DATE, birth_date)
    
    if AGE_CATEGORY_ID in data.keys():
        age_category_id = data[AGE_CATEGORY_ID]
        
        if not age_category_id==None and not DATABASE.check_if_id_exist(AGE_CATEGORIES_DATABASE, int(age_category_id)):
            return NonExistingKey(AGE_CATEGORY_ID, age_category_id)
        member.update_value(AGE_CATEGORY_ID, age_category_id)

    if GENDER in data.keys():
        rating = data[GENDER]
        member.update_value(GENDER, rating)
    
    if MOTHER_ID in data.keys():
        father_id = data[MOTHER_ID]
        
        if not father_id==None and not DATABASE.check_if_id_exist(PARENTS_DATABASE, int(father_id)):
            return NonExistingKey(MOTHER_ID, father_id)
        member.update_value(MOTHER_ID, father_id)
    
    if FATHER_ID in data.keys():
        father_id = data[FATHER_ID]
        
        if not father_id==None and not DATABASE.check_if_id_exist(PARENTS_DATABASE, int(father_id)):
            return NonExistingKey(FATHER_ID, father_id)
        member.update_value(FATHER_ID, father_id)
    
    if DESCRIPTION in data.keys():
        description = data[DESCRIPTION]
        member.update_value(DESCRIPTION, description)
    
    return member


@app.route('/member', methods=['POST'])
def create_member():
    data = get_data_from_request(request)
    member = create_member_instance(data)
    if type(member) == NonExistingKey:
        return str(member)
    try:
        sql_insert, sql_insert_values = member.generate_insert_query()
    except MissingOblitagoryValue as error:
        return str(error)
    response = Member(query = DATABASE.insert(sql_insert, sql_insert_values).data[0])
    flask_response = flask.Response(str(response))
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response


@app.route('/member', methods=['GET'])
def get_member_info():
    sql_select = Member.generate_select_query()
    select_response = DATABASE.select(sql_select)
    response = []
    for item in select_response.data:
        member = Member(query=item)
        response.append(member.__dict__())

    response_str = json.dumps(response, ensure_ascii=False)
    flask_response = flask.Response(response_str)
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response

@app.route('/member/<id>', methods=['PUT'])
def update_member(id: str):
    if id==None or not DATABASE.check_if_id_exist(MEMBERS_DATABASE, int(id)):
        return str(NonExistingKey(ID, id))
    data = get_data_from_request(request)
    member = create_member_instance(data, id)
    if type(member) == NonExistingKey:
        return str(member)
    try:
        sql_insert, sql_insert_values = member.generate_update_query()
    except EmptyRequest as error:
        return str(error)
    print(sql_insert, sql_insert_values)
    response = DATABASE.update(sql_insert, sql_insert_values)

    flask_response = flask.Response(str(response))
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response



@app.route('/member/<id>', methods=['DELETE'])
def delete_member(id: str):
    sql_command: str = f'DELETE FROM {MEMBERS_DATABASE} WHERE id = %s;'
    if id==None or not DATABASE.check_if_id_exist(MEMBERS_DATABASE, int(id)):
        return str(NonExistingKey(ID, id))
    response = DATABASE.delete(sql_command, [id])
    flask_response = flask.Response(str(response))
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response


# ========================== PARENTS ==========================

def create_parent_instance(data: Dict[str, Any], member_id: int = None) -> Parent:
    if not member_id == None:
        parent = Parent(
            id=member_id,
        )
    else:
        parent = Parent()

    # check, if obligatory values provided
    if NAME in data.keys():
        name = data[NAME]
        parent.update_value(NAME, name)
    
    if SURNAME in data.keys():
        surname = data[SURNAME]
        parent.update_value(SURNAME, surname)
    
    if RELATIONSHIP_WITH_CHILD in data.keys():
        relationship_with_child = data[RELATIONSHIP_WITH_CHILD]
        parent.update_value(RELATIONSHIP_WITH_CHILD, relationship_with_child)

    if PHONE in data.keys():
        phone = data[PHONE]
        parent.update_value(PHONE, phone)
    
    if EMAIL in data.keys():
        email = data[EMAIL]
        parent.update_value(EMAIL, email)
    
    return parent


@app.route('/parent', methods=['POST'])
def create_parent():
    data = get_data_from_request(request)
    parent = create_parent_instance(data)
    if type(parent) == NonExistingKey:
        return str(parent)
    try:
        sql_insert, sql_insert_values = parent.generate_insert_query()
    except MissingOblitagoryValue as error:
        return str(error)
    response = Parent(query = DATABASE.insert(sql_insert, sql_insert_values).data[0])
    flask_response = flask.Response(str(response))
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response


@app.route('/parent', methods=['GET'])
def get_parent_info():
    sql_select = Parent.generate_select_query()
    select_response = DATABASE.select(sql_select)
    response = []
    for item in select_response.data:
        member = Parent(query=item)
        response.append(member.__dict__())

    response_str = json.dumps(response, ensure_ascii=False)
    flask_response = flask.Response(response_str)
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response

@app.route('/parent/<id>', methods=['PUT'])
def update_parent(id: str):
    if id==None or not DATABASE.check_if_id_exist(PARENTS_DATABASE, int(id)):
        return str(NonExistingKey(ID, id))
    data = get_data_from_request(request)
    member = create_parent_instance(data, id)
    if type(member) == NonExistingKey:
        return str(member)
    try:
        sql_insert, sql_insert_values = member.generate_update_query()
    except EmptyRequest as error:
        return str(error)
    print(sql_insert, sql_insert_values)
    response = DATABASE.update(sql_insert, sql_insert_values)

    flask_response = flask.Response(str(response))
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response



@app.route('/parent/<id>', methods=['DELETE'])
def delete_parent(id: str):
    sql_command: str = f'DELETE FROM {PARENTS_DATABASE} WHERE id = %s;'
    if id==None or not DATABASE.check_if_id_exist(PARENTS_DATABASE, int(id)):
        return str(NonExistingKey(ID, id))
    response = DATABASE.delete(sql_command, [id])
    flask_response = flask.Response(str(response))
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response







if __name__ == '__main__':
    Flask.run(app, host='0.0.0.0', port='8888', debug=True)