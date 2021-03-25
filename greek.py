from fastapi import FastAPI, APIRouter
from interfaces.mysql import Mysql
from interfaces.mongo import Mongo
import logging

import decorators


greekr = APIRouter()



# Mysql Routes - Greek vocab/charts/etc DB CRUD handling
@greekr.get('/greek/showdbs')
def showdbs():
    return greek().showdbs()

@greekr.get('/greek/showtables')
def showtables(db):
    return greek(db).showtables()

@greekr.post('/greek/vocab')
def postvocab(greek_regularized, definition, part_of_speech,
        principal_parts=None, diacritics=None):
    return greek().postvocab(greek_regularized, definition, 
        part_of_speech, principal_parts=None, diacritics=None)

@greekr.get('/greek/vocab')
@decorators.sanitize
def getvocab(part_of_speech, term=None):
    return greek().getvocab(part_of_speech, term)



# Mongo Routes - User DB CRUD handling
@greekr.get('/users/listdbs')
def listdbs():
    return users(None).listdbs()

@greekr.get('/users/listcollections')
def listcollections(db):
    return users(db).listcollections()

@greekr.get('/users/listdocs')
@decorators.sanitize
def listdocs(db, collection, limit=1000):
    print(type(limit))
    return users(db).listdocs(collection, limit)

@greekr.get('/users/simplesearch')
@decorators.sanitize
def simplesearch(db, collection, key, value):
    return users(db).simplesearch(collection, key, value)

@greekr.post('/users/postuser')
def postuser(db, collection, email, name, pw):
    return users(db).postuser(db, collection, email, name, pw)

@greekr.post('/users/login')
def login(email, pw):
    return users('greekuserdb').login(email, pw)


class greek(Mysql):

    def showdbs(self):
        """ Displays existing databases  """
    
        self.cursor.execute("SHOW DATABASES")
        dbs = [db[0] for db in self.cursor]
        self.cnx.close()
        self.logger.info('MF hi')
        return dbs
    

    def showtables(self):
        """ Displays all tables in provided db """
    
        self.cursor.execute("SHOW TABLES;")
        tables = [table[0] for table in self.cursor]
        self.cnx.close()
        return tables
    
    
    def postvocab(self, greek_regularized, definition, part_of_speech,
             principal_parts=None, diacritics=None):
        """ add a noun to the greek vocab database """
    
        self.cursor.execute(f"INSERT INTO {part_of_speech} VALUES("
            "'{greek_regularized}', '{principal_parts}', "
            "'{diacritics}', '{definition}');")
        self.cnx.commit()
        res = getvocab(greek_regularized, part_of_speech)
        self.cnx.close()
        return res
    

    def getvocab(self, part_of_speech, term=None):
        """ Retrieve a row by Primary Key - regularized greek """
        
        self.cursor.execute(f'USE greekvocab;')
        if term:
            self.cursor.execute(f"SELECT * FROM {part_of_speech} WHERE regular" 
                "= '{term}';")
            print(term)
        else:
            self.cursor.execute(f"SELECT * FROM {part_of_speech};")
        keys = ['greek_regularized', 'principal_parts', 
            'diacritics', 'definition']
        rows = { zip(keys, term) for term in self.cursor }
        self.cnx.close()
        return rows


    def __init__(self, db=None):
        self.logger = self.log(__name__)
        self.logger.info('mysql objected created')
        self.cnx = self.__connect(db)
        self.cursor = self.cnx.cursor()
    
    def __connect(self, db=None):
        ''' Stateless connection - with Redis, handle single connection
        creation, check, timeout & release adding state in Redis '''
    
        cnx = Mysql().connect(db)
        return cnx



class users(Mongo):

    def listdbs(self):
        return self.cnx.database_names()


    def listcollections(self):
        return self.dbo.list_collection_names()


    def listdocs(self, collection, limit):
        coll = self.dbo[collection]
        doclist = [str(x) for x in coll.find({}).limit(limit)]
        return doclist


    def simplesearch(self, collection, key, value):
        ''' supply single search parameter as key & value '''

        coll = self.dbo[collection]
        res = coll.find_one({key:value}, {'_id': False})

        return res


    def postuser(self, db, collection, email, name, pw):

        coll = self.dbo[collection]
        if coll.insert_one({'email':email, 'name':name, 'pw':pw}):
            return users(db).simplesearch(collection, 'email', email)
        return 'error encountered'


    def login(self, email, pw):
        coll = self.dbo['users']
        res = simplesearch('greekuserdb', 'users', 'email', email)
        print(res)
        if pw == res['pw']:
            return res['name']
        return {'success': False}


    def __init__(self, db=None):
        self.logger = self.log(__name__)
        self.logger.info('mongodb objected created')
        self.cnx = self.__connect()
        if db:
            self.dbo = self.cnx[db]

    
    def __connect(self, db=None):
        ''' Stateless connection - with Redis, handle single connection
        creation, check, timeout & release adding state in Redis '''
    
        cnx = Mongo().connect()
        return cnx

