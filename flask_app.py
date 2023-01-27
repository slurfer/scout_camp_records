from datetime import datetime
from flask import Flask, request, abort, Request, jsonify
import flask
import json
from typing import Dict, Tuple, List, Any
from flask_cors import CORS
from member import Member
from parent import Parent
from age_category import AgeCategory
from constants import *
from tour_de_app_database import TourDeAppDatabase
from classes import *
from Errors import *
from camp import Camp
from participant import Participant

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


def check_roreign_keys(data: Dict[str, Any], foreings_keys):
    for id_to_check in foreings_keys:
        if id_to_check[0] in data:
            id = data[id_to_check[0]]
            table_name = id_to_check[1]
            if not DATABASE.check_if_id_exist(table_name, id) and not id == None:
                raise NonExistingKey(table_name, id)
    return None

# ========================== MEMBERS ==========================


@app.route('/member', methods=['POST'])
def create_member():
    data = get_data_from_request(request)
    try:
        check_roreign_keys(data, Member.FOREIGN_KEYS)
    except NonExistingKey as error:
        return str(error)

    member = Member(request=data)
    
    try:
        sql_insert, sql_insert_values = member.generate_insert_query()
    except MissingOblitagoryValue as error:
        return str(error)
    response = Member(query = DATABASE.insert(sql_insert, sql_insert_values).data[0])
    try:
        handle_participants_changes_for_member(response.values[ID].value, member.values[CAMP_IDS].value)
    except NonExistingKey as error:
        return str(error)
    response.values[CAMP_IDS].value = get_member_camp_ids(response.values[ID].value)
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
        member.values[CAMP_IDS].value = get_member_camp_ids(member.values[ID].value)
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
    try:
        check_roreign_keys(data, Member.FOREIGN_KEYS)
    except NonExistingKey as error:
        return str(error)

    member = Member(request=data, id=id)

    try:
        sql_insert, sql_insert_values = member.generate_update_query()
        response = DATABASE.update(sql_insert, sql_insert_values)
        flask_response = flask.Response(str(response))
        flask_response.headers['Access-Control-Allow-Origin'] = '*'
    except EmptyRequest as error:
        flask_response = str(error)
    

    if not member.values[CAMP_IDS].value == None:
        try:
            handle_participants_changes_for_member(member.values[ID].value, member.values[CAMP_IDS].value)
        except NonExistingKey as error:
            return str(error)
        flask_response = 'Item updated'
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

    parent = Parent(request=data, id=id)

    try:
        sql_insert, sql_insert_values = parent.generate_update_query()
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


# ========================== CAMPS ==========================

@app.route('/camp', methods=['POST'])
def create_camp():
    data = get_data_from_request(request)

    try:
        check_roreign_keys(data, Camp.FOREIGN_KEYS)
    except NonExistingKey as error:
        return str(error)

    camp = Camp(request=data)

    try:
        sql_insert, sql_insert_values = camp.generate_insert_query()
    except MissingOblitagoryValue as error:
        return str(error)
    response = Camp(query = DATABASE.insert(sql_insert, sql_insert_values).data[0])
    flask_response = flask.Response(str(response))
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response


@app.route('/camp', methods=['GET'])
def get_camp_info():
    sql_select = Camp.generate_select_query()
    select_response = DATABASE.select(sql_select)
    response = []
    for item in select_response.data:
        member = Camp(query=item)
        response.append(member.__dict__())

    response_str = json.dumps(response, ensure_ascii=False)
    flask_response = flask.Response(response_str)
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response

@app.route('/camp/<id>', methods=['PUT'])
def update_camp(id: str):
    if id==None or not DATABASE.check_if_id_exist(CAMPS_DATABASE, int(id)):
        return str(NonExistingKey(ID, id))
    data = get_data_from_request(request)

    try:
        check_roreign_keys(data, Camp.FOREIGN_KEYS)
    except NonExistingKey as error:
        return str(error)

    camp = Camp(request=data, id=id)

    try:
        sql_insert, sql_insert_values = camp.generate_update_query()
    except EmptyRequest as error:
        print(error)
        return str(error)
    response = DATABASE.update(sql_insert, sql_insert_values)

    flask_response = flask.Response(str(response))
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response



@app.route('/camp/<id>', methods=['DELETE'])
def delete_camp(id: str):
    sql_command: str = f'DELETE FROM {CAMPS_DATABASE} WHERE id = %s;'
    if id==None or not DATABASE.check_if_id_exist(CAMPS_DATABASE, int(id)):
        return str(NonExistingKey(ID, id))
    response = DATABASE.delete(sql_command, [id])
    flask_response = flask.Response(str(response))
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response


# ========================== PARTICIPANTS ==========================
@app.route('/test', methods=['get'])
def test():
    # return str(create_participant(3, 2))
    # return str(get_member_camp_ids(2))
    # return str(delete_participant(2))
    return str(handle_participants_changes_for_member(1, [1, 3, 2]))

def handle_participants_changes_for_member(member_id:int, camp_ids: List[int]):
    delete_participant(member_id)
    for camp_id in camp_ids:
        create_participant(member_id, camp_id)
    return get_member_camp_ids(member_id)

def check_participants_foreign_keys(member_id: int = None, camp_id: int = None):
    if not member_id==None and not DATABASE.check_if_id_exist(MEMBERS_DATABASE, member_id):
        raise NonExistingKey(MEMBERS_DATABASE, member_id)
    if not camp_id==None and not DATABASE.check_if_id_exist(CAMPS_DATABASE, camp_id):
        raise NonExistingKey(CAMPS_DATABASE, camp_id)

def create_participant(member_id: int, camp_id: int):
    check_participants_foreign_keys(member_id, camp_id)

    participant = Participant(member_id=member_id, camp_id=camp_id)

    sql_insert, sql_insert_values = participant.generate_insert_query()
    return Participant(query = DATABASE.insert(sql_insert, sql_insert_values).data[0])


def get_member_camp_ids(member_id):
    check_participants_foreign_keys(member_id)

    participant = Participant(member_id=member_id)

    sql_insert, sql_insert_values = participant.generate_get_all_camps_query()
    respose = DATABASE.select(sql_insert, sql_insert_values).data
    camp_ids = []
    for tuple in respose:
        camp_ids.append(tuple[0])
    return camp_ids


def delete_participant(member_id: str):
    sql_command: str = f'DELETE FROM {PARTICIPANTS_DATABASE} WHERE member_id = %s;'
    if member_id==None or not DATABASE.check_if_id_exist(MEMBERS_DATABASE, int(member_id)):
        return str(NonExistingKey(ID, member_id))
    return DATABASE.delete(sql_command, [member_id])


# ========================== AGE_CATEGORIES ==========================

@app.route('/age_category', methods=['POST'])
def create_age_category():
    data = get_data_from_request(request)


    age_category = AgeCategory(request=data)

    try:
        sql_insert, sql_insert_values = age_category.generate_insert_query()
    except MissingOblitagoryValue as error:
        return str(error)
    response = AgeCategory(query = DATABASE.insert(sql_insert, sql_insert_values).data[0])
    flask_response = flask.Response(str(response))
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response


@app.route('/age_category', methods=['GET'])
def get_age_category_info():
    sql_select = AgeCategory.generate_select_query()
    select_response = DATABASE.select(sql_select)
    response = []
    for item in select_response.data:
        age_category = AgeCategory(query=item)
        response.append(age_category.__dict__())

    response_str = json.dumps(response, ensure_ascii=False)
    flask_response = flask.Response(response_str)
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response

@app.route('/age_category/<id>', methods=['PUT'])
def update_age_category(id: str):
    if id==None or not DATABASE.check_if_id_exist(AGE_CATEGORIES_DATABASE, int(id)):
        return str(NonExistingKey(ID, id))
    data = get_data_from_request(request)

    age_category = AgeCategory(request=data, id=id)

    try:
        sql_insert, sql_insert_values = age_category.generate_update_query()
    except EmptyRequest as error:
        print(error)
        return str(error)
    print(sql_insert, sql_insert_values)
    response = DATABASE.update(sql_insert, sql_insert_values)

    flask_response = flask.Response(str(response))
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response



@app.route('/age_category/<id>', methods=['DELETE'])
def delete_age_category(id: str):
    sql_command: str = f'DELETE FROM {AGE_CATEGORIES_DATABASE} WHERE id = %s;'
    if id==None or not DATABASE.check_if_id_exist(AGE_CATEGORIES_DATABASE, int(id)):
        return str(NonExistingKey(ID, id))
    response = DATABASE.delete(sql_command, [id])
    flask_response = flask.Response(str(response))
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response





if __name__ == '__main__':
    Flask.run(app, host='0.0.0.0', port='8888', debug=True)