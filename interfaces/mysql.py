from __future__ import annotations
import sys, os
import mysql.connector as mc
import logging
from fastapi import FastAPI, APIRouter


mysqlr = APIRouter()


class Mysql():
    def __init__(self):
        pass
   
    @staticmethod 
    @mysqlr.get('/mysql/listdbs')
    def listdbs(showtables: bool =False) -> list:
        ''' return all present databases in form of list '''
        pass

    
    @staticmethod 
    @mysqlr.get('/mysql/listtables')
    def listtables(db: str) -> list:
        ''' return all present tables in form of a list '''
        pass


    @staticmethod 
    @mysqlr.get('/mysql/listcolumns')
    def listcolumns(db: str, table: str) -> list:
        ''' not all Database Systems have functional column 
        equivalent - return all columns of a dictionary as a list '''
        pass


    @staticmethod 
    @mysqlr.get('/mysql/listrow')
    def listrow(db: str, table: str, key) -> list:
        ''' Return the data from a row by matching in list form '''
        pass


    @staticmethod 
    @mysqlr.get('/mysql/listrows')
    def listrows(db: str, table: str, key) -> [list]:
        ''' Return the data from one or several rows by matching
        in list of lists form '''
        pass 


    @staticmethod 
    @mysqlr.get('/mysql/dictrow')
    def dictrow(db: str, table: str, key) -> dict:
        ''' Return the data from a row by matching in dict form '''
        pass


    @staticmethod 
    @mysqlr.get('/mysql/dictrows')
    def dictrows(db: str, table: str, key) -> {dict}:
        ''' Return the data from one or several rows by matching 
        in dict of dicts form '''
        pass


    @staticmethod 
    @mysqlr.post('/mysql/postrows')
    def postrow(db: str, table: str, **kwargs: str) -> bool:
        ''' post one or many new rows or equivalent in format
        'key'=['col1', 'col2',...] '''
        pass


    def __init__(self) -> None:
        pass


    def log(self, name):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s:%(levelname)s:%(name)s - %(message)s')
        handler = logging.FileHandler(f'logs/{name}.log')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger


    def connect(self, db=None) -> mc.connect:
        try:
            cnx = mc.connect(user=os.getenv('dbuser'),
                    password=os.getenv('dbpw'), db=db,
                    auth_plugin='mysql_native_password')
            return cnx
        except mc.Error as e:
            print(e)





