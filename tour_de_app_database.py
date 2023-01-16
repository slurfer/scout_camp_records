import mysql.connector
from typing import Dict, Tuple, List, Any
from login import *
from flask import Response
from database_table import DatabaseTable
from Errors import *
from constants import *
from classes import *


def connect_to_database():
    mydb = mysql.connector.connect(
        host=HOST,
        user=DATABASE_USER,
        password=PASSWORD,
        database = DATABASE
    )

    mycursor = mydb.cursor()

    return mydb, mycursor


def close_database(mydb, mycursor):
    mycursor.close()
    mydb.close()



class TourDeAppDatabase:
    
    def select(self, sql_command: str) -> SelectQueryResponse:
        # -------- create connection --------
        database, cursor = connect_to_database()
        
        # -------- execute command --------
        cursor.execute(sql_command)
        response = cursor.fetchall()
        
        # -------- close connection --------
        cursor.close()
        database.close()
        return SelectQueryResponse(response)
        
    
    def insert(self, sql_command: str, sql_values: List[Any], commit:bool = True) -> SelectQueryResponse:
        # -------- create connection --------
        database, cursor = connect_to_database()

        # -------- execute command --------
        cursor.execute(sql_command, sql_values)
        if commit:
            database.commit()
        else:
            print('Skipping commit.')
        table_name = sql_command.split()[2]
        last_added_item = self.get_last_added_item(table_name, cursor)
        
        # -------- close connection --------
        cursor.close()
        database.close()
        return SelectQueryResponse(last_added_item)
    
    def update(self, sql_command: str, sql_values: List[Any], commit:bool = True) -> DatabaseOperationResult:
        # -------- create connection --------
        database, cursor = connect_to_database()

        # -------- execute command --------
        cursor.execute(sql_command, sql_values)
        if commit:
            database.commit()
        else:
            print('Skipping commit.')
        
        # -------- close connection --------
        cursor.close()
        database.close()
        return DatabaseOperationResult('Item updated')
    
    def delete(self, sql_command: str, sql_values: List[Any], commit:bool = True) -> DatabaseOperationResult:
        # -------- create connection --------
        database, cursor = connect_to_database()

        # -------- execute command --------
        cursor.execute(sql_command, sql_values)
        if commit:
            database.commit()
        else:
            print('Skipping commit.')
        
        # -------- close connection --------
        cursor.close()
        database.close()
        return DatabaseOperationResult('Item deleted')

    def get_last_added_item(self, table_name: str, cursor):
        item_id = str(cursor.lastrowid)
        query = f'SELECT * FROM {table_name} WHERE id=%s'
        cursor.execute(query, [item_id])
        response = cursor.fetchall()
        return response
    
    def check_if_id_exist(self, table_name: str, id: int):
        # -------- create connection --------
        database, cursor = connect_to_database()

        # -------- get all ids from table --------
        sql_command = f'SELECT {ID} FROM {table_name};'
        cursor.execute(sql_command)
        response = cursor.fetchall()

        # -------- check if value exist --------
        for item in response:
            if id == item[0]:
                close_database(database, cursor)
                return True
        return False



