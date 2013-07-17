from Model import Model
import sqlite3
import os

class UserOptionsDB(Model):
    def __init__(self,root='',database_path='data/',database_name='mydatabase.db'):
        Model.__init__(self,root,database_path,database_name)
        self.name = 'user_options'
        self.columns = {'user_key': 'TEXT PRIMARY KEY'}
        self.columns['user_value'] = 'TEXT KEY'

    def read(self,key):
        self.open()
        values = self.select(cols=['user_value'],where={'user_key':key})
        self.close()
        if values == {}:
            return None
        else:
            return eval(values['user_value'][0])

    def write(self,key,value):
        self.open()
        values = self.select(cols=['user_value'],where={'user_key':key})
        #print values
        if values != {}:
            self.update({'user_key':key},{'user_value':repr(value)})
            return True

        out = self.insert({'user_key':key,'user_value':repr(value)})
        self.close()
        return out
        

