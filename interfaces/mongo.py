from __future__ import annotations
import sys, os
from pymongo import MongoClient
import logging
from fastapi import FastAPI, APIRouter


mongor = APIRouter()


class Mongo():
    def __init__(self):
        pass

    @staticmethod
    @mongor.get('/mongo/listdbs')
    def listdbs(showtables: bool =False) -> list:
        ''' return all present databases in for of list '''
        pass


    def log(self, name) -> logger:
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s:%(levelname)s:%(name)s - %(message)s')
        handler = logging.FileHandler(f'logs/{__name__}.log')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger


    def connect(self) -> MongoClient:
        client = MongoClient()
        client = MongoClient('127.0.0.1', 27017)
        return client
