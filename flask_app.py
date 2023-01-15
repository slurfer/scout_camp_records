from datetime import datetime
from flask import Flask, request, abort, Request, jsonify
import flask
import json
from typing import Dict, Tuple, List, Any
from flask_cors import CORS
from record import Record
from programmer import Programmer
from tag import Tag
from tagged_record import TaggedRecord
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


# ========================== RECORDS ==========================

def create_record_instance(data: Dict[str, Any], tag_id: int = None) -> Record:
    if not tag_id == None:
        record = Record(
            id=tag_id,
        )
    else:
        record = Record()

    # check, if obligatory values provided
    if DATETIME in data.keys():
        datetime = data[DATETIME]
        record.update_value(DATETIME, datetime)
    
    if PROGRAMMING_LANGUAGE in data.keys():
        programming_language = data[PROGRAMMING_LANGUAGE]
        record.update_value(PROGRAMMING_LANGUAGE, programming_language)
    
    if MINUTES_SPENT in data.keys():
        minutes_spent = data[MINUTES_SPENT]
        record.update_value(MINUTES_SPENT, minutes_spent)
    
    if RATING in data.keys():
        rating = data[RATING]
        record.update_value(RATING, rating)
    
    if PROGRAMMER_ID in data.keys():
        programmer_id = data[PROGRAMMER_ID]
        
        if not programmer_id==None and not DATABASE.check_if_id_exist(PROGRAMMERS_DATABASE, int(programmer_id)):
            return NonExistingKey(PROGRAMMER_ID, programmer_id)
        record.update_value(PROGRAMMER_ID, programmer_id)
    
    if TAG_IDS in data.keys():
        tag_ids_input = data[TAG_IDS]
        if not tag_ids_input == None:
            # -------- check if all provided are valid --------
            tag_ids = []
            for tag_id in tag_ids_input:
                if DATABASE.check_if_id_exist(TAGS_DATABASE, int(tag_id)):
                    tag_ids.append(tag_id)
                else:
                    return NonExistingKey(TAG_IDS, tag_id)
        else:
            tag_ids = tag_ids_input
        print(tag_ids)
        record.update_value(TAG_IDS, tag_ids)
    
    if DESCRIPTION in data.keys():
        description = data[DESCRIPTION]
        record.update_value(DESCRIPTION, description)
    
    return record


@app.route('/record', methods=['POST'])
def create_record():
    data = get_data_from_request(request)
    record = create_record_instance(data)
    if type(record) == NonExistingKey:
        return str(record)
    sql_insert, sql_insert_values = record.generate_insert_query()
    response = Record(query = DATABASE.insert(sql_insert, sql_insert_values).data[0])
    flask_response = flask.Response(str(response))
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response


@app.route('/record', methods=['GET'])
def get_record_info():
    sql_select = Record.generate_select_query()
    select_response = DATABASE.select(sql_select)
    response = []
    for item in select_response.data:
        record = Record(query=item)
        # -------- check if all tag_ids exists --------
        if not record.values[TAG_IDS].value == None:
            tag_ids = []
            for key in record.values[TAG_IDS].value:
                if DATABASE.check_if_id_exist(TAGS_DATABASE, int(key)):
                    tag_ids.append(key)
            if len(tag_ids) == 0:
                tag_ids = None
            record.update_value(TAG_IDS, tag_ids)
        response.append(record.__dict__())

    response_str = json.dumps(response, ensure_ascii=False)
    flask_response = flask.Response(response_str)
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response

@app.route('/record/<id>', methods=['PUT'])
def update_record(id: str):
    if id==None or not DATABASE.check_if_id_exist(RECORDS_DATABASE, int(id)):
        return str(NonExistingKey(ID, id))
    data = get_data_from_request(request)
    record = create_record_instance(data, id)
    if type(record) == NonExistingKey:
        return str(record)
    try:
        sql_insert, sql_insert_values = record.generate_update_query()
    except EmptyRequest as error:
        return str(error)
    print(sql_insert, sql_insert_values)
    response = DATABASE.update(sql_insert, sql_insert_values)

    flask_response = flask.Response(str(response))
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response



@app.route('/record/<id>', methods=['DELETE'])
def delete_record(id: str):
    sql_command: str = f'DELETE FROM {RECORDS_DATABASE} WHERE id = %s;'
    if id==None or not DATABASE.check_if_id_exist(RECORDS_DATABASE, int(id)):
        return str(NonExistingKey(ID, id))
    response = DATABASE.delete(sql_command, [id])
    flask_response = flask.Response(str(response))
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response



# ========================== PROGRAMMER ==========================

def create_programmer_instance(data: Dict[str, Any], id: int = None) -> Record:
    if not id == None:
        programmer = Programmer(
            id=id,
        )
    else:
        programmer = Programmer()
    
    if NAME in data.keys():
        name = data[NAME]
        programmer.update_value(NAME, name)
    
    if SURNAME in data.keys():
        surname = data[SURNAME]
        programmer.update_value(SURNAME, surname)

    return programmer


@app.route('/programmer', methods=['POST'])
def create_programmer():
    data = get_data_from_request(request)
    programmer = create_programmer_instance(data)
    sql_insert, sql_insert_values = programmer.generate_insert_query()
    response = Programmer(query = DATABASE.insert(sql_insert, sql_insert_values).data[0])

    flask_response = flask.Response(str(response))
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response


@app.route('/programmer', methods=['GET'])
def get_programmer_info():
    sql_select = Programmer.generate_select_query()
    select_response = DATABASE.select(sql_select)
    response = []
    for item in select_response.data:
        programmer = Programmer(query=item)
        response.append(programmer.__dict__())

    response_str = json.dumps(response, ensure_ascii=False)
    flask_response = flask.Response(response_str)
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response

@app.route('/programmer/<id>', methods=['PUT'])
def update_programmer(id: str):
    if id==None or not DATABASE.check_if_id_exist(PROGRAMMERS_DATABASE, int(id)):
        return str(NonExistingKey(ID, id))
    data = get_data_from_request(request)
    programmer = create_programmer_instance(data, id)
    try:
        sql_insert, sql_insert_values = programmer.generate_update_query()
    except EmptyRequest as error:
        return str(error)
    response = DATABASE.update(sql_insert, sql_insert_values)

    flask_response = flask.Response(str(response))
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response



@app.route('/programmer/<id>', methods=['DELETE'])
def delete_programmer(id: str):
    sql_command: str = f'DELETE FROM {PROGRAMMERS_DATABASE} WHERE id = %s;'
    if id==None or not DATABASE.check_if_id_exist(PROGRAMMERS_DATABASE, int(id)):
        return str(NonExistingKey(ID, id))
    response = DATABASE.delete(sql_command, [id])

    flask_response = flask.Response(str(response))
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response


# ========================== TAG ==========================

def create_tag_instance(data: Dict[str, Any], id: int = None) -> Record:
    if not id == None:
        tag = Tag(
            id=id,
        )
    else:
        tag = Tag()
    
    if NAME in data.keys():
        name = data[NAME]
        tag.update_value(NAME, name)
    
    if COLOR in data.keys():
        color = data[COLOR]
        tag.update_value(COLOR, color)

    if DESCRIPTION in data.keys():
        description = data[DESCRIPTION]
        tag.update_value(DESCRIPTION, description)

    return tag


@app.route('/tag', methods=['POST'])
def create_tag():
    data = get_data_from_request(request)
    tag = create_tag_instance(data)
    try:
        sql_insert, sql_insert_values = tag.generate_insert_query()
    except MissingOblitagoryValue as error:
        return str(error)
    response = Tag(query = DATABASE.insert(sql_insert, sql_insert_values).data[0])

    flask_response = flask.Response(str(response))
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response


@app.route('/tag', methods=['GET'])
def get_tag_info():
    sql_select = Tag.generate_select_query()
    select_response = DATABASE.select(sql_select)
    response = []
    for item in select_response.data:
        tag = Tag(query=item)
        response.append(tag.__dict__())

    response_str = json.dumps(response, ensure_ascii=False)
    flask_response = flask.Response(response_str)
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response

@app.route('/tag/<id>', methods=['PUT'])
def update_tag(id: str):
    if id==None or not DATABASE.check_if_id_exist(TAGS_DATABASE, int(id)):
        return str(NonExistingKey(ID, id))
    data = get_data_from_request(request)
    tag = create_tag_instance(data, id)
    try:
        sql_insert, sql_insert_values = tag.generate_update_query()
    except EmptyRequest as error:
        return str(error)
    response = DATABASE.update(sql_insert, sql_insert_values)

    flask_response = flask.Response(str(response))
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response



@app.route('/tag/<id>', methods=['DELETE'])
def delete_tag(id: str):
    sql_command: str = f'DELETE FROM {TAGS_DATABASE} WHERE id = %s;'
    if id==None or not DATABASE.check_if_id_exist(TAGS_DATABASE, int(id)):
        return str(NonExistingKey(ID, id))
    response = DATABASE.delete(sql_command, [id])

    flask_response = flask.Response(str(response))
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response


# ========================== TAGGED_RECORDS ==========================

def create_tagged_record_instance(data: Dict[str, Any], id: int = None) -> Record:
    if not id == None:
        tagged_record = TaggedRecord(
            id=id,
        )
    else:
        tagged_record = TaggedRecord()

    # check, if obligatory values provided
    if RECORD_ID in data.keys():
        record_id = data[RECORD_ID]
        
        if not DATABASE.check_if_id_exist(RECORDS_DATABASE, int(record_id)):
            return NonExistingKey(RECORD_ID, record_id)
        tagged_record.update_value(RECORD_ID, record_id)
    
    if TAG_ID in data.keys():
        tag_id = data[TAG_ID]
        
        if not DATABASE.check_if_id_exist(TAGS_DATABASE, int(tag_id)):
            return NonExistingKey(TAG_ID, tag_id)
        tagged_record.update_value(TAG_ID, tag_id)
    
    return tagged_record


@app.route('/tagged_record', methods=['POST'])
def create_tagged_record():
    data = get_data_from_request(request)
    tagged_record = create_tagged_record_instance(data)
    if type(tagged_record) == NonExistingKey:
        return str(tagged_record)
    sql_insert, sql_insert_values = tagged_record.generate_insert_query()
    response = TaggedRecord(query = DATABASE.insert(sql_insert, sql_insert_values).data[0])
    flask_response = flask.Response(str(response))
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response


@app.route('/tagged_record', methods=['GET'])
def get_tagged_record_info():
    sql_select = TaggedRecord.generate_select_query()
    select_response = DATABASE.select(sql_select)
    response = []
    for item in select_response.data:
        record = TaggedRecord(query=item)
        response.append(record.__dict__())

    response_str = json.dumps(response, ensure_ascii=False)
    flask_response = flask.Response(response_str)
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response

@app.route('/tagged_record/<id>', methods=['PUT'])
def update_tagged_record(id: str):
    if id==None or not DATABASE.check_if_id_exist(TAGGED_RECORDS_DATABASE, int(id)):
        return str(NonExistingKey(ID, id))
    data = get_data_from_request(request)
    tagged_record = create_tagged_record_instance(data, id)
    if type(tagged_record) == NonExistingKey:
        return str(tagged_record)
    try:
        sql_insert, sql_insert_values = tagged_record.generate_update_query()
    except EmptyRequest as error:
        return str(error)
    print(sql_insert, sql_insert_values)
    response = DATABASE.update(sql_insert, sql_insert_values)

    flask_response = flask.Response(str(response))
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response



@app.route('/tagged_record/<id>', methods=['DELETE'])
def delete_tagged_record(id: str):
    sql_command: str = f'DELETE FROM {TAGGED_RECORDS_DATABASE} WHERE id = %s;'
    if id==None or not DATABASE.check_if_id_exist(TAGGED_RECORDS_DATABASE, int(id)):
        return str(NonExistingKey(ID, id))
    response = DATABASE.delete(sql_command, [id])
    flask_response = flask.Response(str(response))
    flask_response.headers['Access-Control-Allow-Origin'] = '*'
    return flask_response




if __name__ == '__main__':
    Flask.run(app, host='0.0.0.0', port='8888', debug=True)