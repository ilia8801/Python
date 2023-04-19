#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
Модуль подключения к БД postgresql для получения результата от sql запроса
'''

import psycopg2
from typing import List, Any
from get_config import Config
from config import (dblist,conn_label)
 

class Query:

    def __init__(self,
                 file: str,
                 config_file: str = None
                 ):
        self.select_db = str([val['dbsource'] for key,val in dblist.items() ]).replace("']","").replace("['","")
        self.db_param_connection = str([val['connection'] for key,val in conn_label.items() if self.select_db in key ]).replace("']","").replace("['","")
         
        self.query_file = 'source/query/query_1' + '.sql'
        self.query = self.read_query(self.query_file)
        connection = None
        try:
            connection = psycopg2.connect(self.db_param_connection)
            cursor = connection.cursor()
            cursor.execute(self.query)
            rows = cursor.fetchall()
        except psycopg2.Error as er:
            raise er
        finally:
            if connection:
                print("Подключение к БД работает...")
                connection.close()
             
        self.rows = []
        self.td_rows = []
   
    #Чтение запроса из файла, возврат в формате строки
    def read_query(self,
                   file: str) -> str:
        with open(file, "r", -1, "utf-8") as fp:
            try:
                query = fp.read()
            except Exception as e:
                print("\n sql.py - Не удается прочитать файл {}\
                       \n ".format(self.query_file), e)
        return query
   
    #Возврат результата запроса в формате кортежа списков
    def get_rows(self) -> List[List[Any]]:
        return self.td_rows       
    
    #Выполнение запроса, и получение результата в формате кортежа списков
    def exec_query(self):
        try:
           with psycopg2.connect(self.db_param_connection) as session:
                with session.cursor() as cursor:
                    try:
                        connection = psycopg2.connect(self.db_param_connection)    
                        cursor = connection.cursor()
                        cursor.execute(self.query)
                        self.rows = cursor.fetchall()
                        for row in self.rows:
                            self.temp_list = []
                            for row_cell in range(0, len(row)):
                                self.temp_list.append(row[row_cell])
                            self.td_rows.append(self.temp_list)
                        del self.temp_list
                        print(self.rows)
                    except Exception as e:
                        print("\n sql.py - Не удается получить результат запроса - \
                               {} \n ".format(self.query_file), e)
        except Exception as e:
            print("\n sql.py - Не удается инициализировать подключение к БД -  \
                   {} \n ".format(self.query_file), e)
        return self