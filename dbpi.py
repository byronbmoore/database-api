from __future__   import annotations
from abc          import ABC, abstractmethod
from fastapi      import FastAPI
import os
import logging

import interfaces.mysql
import interfaces.mongo
import greek



''' DB-PI 
This is a pan-database wrapper service for consumption by database
type/style agnostic scripts and other services. Goal is to interact
with multiple databases without the need to know/implement in client
code, also reducing the spread of databases and concentrating 
footprint to potentially one machine rather than a poorly documented
flock of DBs. '''



''' Instantiate service routers - each fulfills role of a different
service to a different database or db software
'''

app = FastAPI()
app.include_router(greek.greekr)
app.include_router(interfaces.mongo.mongor)
app.include_router(interfaces.mysql.mysqlr)


class idbwrap(ABC):
    ''' Abstract Class for Database-Wrapping API service '''

    @abstractmethod
    #@app.get('/listdbs')
    def listdbs(self, showtables: bool =False) -> list:
        ''' return all present databases in form of list '''
        pass

    
    @abstractmethod
    #@app.get('/listtables')
    def listtables(self, db: str) -> list:
        ''' return all present tables in form of a list '''
        pass


    #@app.get('/listcolumns')
    def listcolumns(self, db: str, table: str) -> list:
        ''' not all Database Systems have functional column 
        equivalent - return all columns of a dictionary as a list '''
        pass


    @abstractmethod
    #@app.get('/listrow')
    def listrow(self, db: str, table: str, key) -> list:
        ''' Return the data from a row by matching in list form '''
        pass


    @abstractmethod
    #@app.get('listrows')
    def listrows(self, db: str, table: str, key) -> [list]:
        ''' Return the data from one or several rows by matching
        in list of lists form '''
        pass 


    @abstractmethod
    #@app.get('/dictrow')
    def dictrow(self, db: str, table: str, key) -> dict:
        ''' Return the data from a row by matching in dict form '''
        pass


    @abstractmethod
    #@app.get('/dictrows')
    def dictrows(self, db: str, table: str, key) -> {dict}:
        ''' Return the data from one or several rows by matching 
        in dict of dicts form '''
        pass

    @abstractmethod
    #@app.post('/postrows')
    def postrow(self, db: str, table: str, **kwargs: str) -> bool:
        ''' post one or many new rows or equivalent in format
        'key'=['col1', 'col2',...] '''
        pass


    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def connect(self):
        pass











