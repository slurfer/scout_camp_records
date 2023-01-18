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
def check_relationship_connections_member(data: Dict[str, Any]):
    ids_to_check = [
        (AGE_CATEGORY_ID, AGE_CATEGORIES_DATABASE),
        (MOTHER_ID, PARENTS_DATABASE),
        (FATHER_ID, PARENTS_DATABASE),
    ]
    for id_to_check in ids_to_check:
        if id_to_check[0] in data:
            id = data[id_to_check[0]]
            table_name = id_to_check[1]
            if not DATABASE.check_if_id_exist(table_name, id):
                raise NonExistingKey(table_name, id)

@app.route('/member', methods=['POST'])
def create_member():
    data = get_data_from_request(request)
    try:
        check_relationship_connections_member(data)
    except NonExistingKey as error:
        return str(error)

    member = Member(request=data)
    
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
    member = Member(request=data, id=id)
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

@app.route('/parent', methods=['POST'])
def create_parent():
    data = get_data_from_request(request)
    parent = Parent(request=data)
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
    member = Parent(request=data, id=id)
    print(member)
    if type(member) == NonExistingKey:
        return str(member)
    try:
        sql_insert, sql_insert_values = member.generate_update_query()
    except EmptyRequest as error:
        print(error)
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