from Model import Model
import sqlite3
import os

class TimeTableDB(Model):
    def __init__(self,root='',database_path='data/',database_name='mydatabase.db'):
        Model.__init__(self,root,database_path,database_name)
        self.name = 'time_table'
        self.columns['semester'] = 'INTEGER'
        self.columns['permutation'] = 'INTEGER'
        self.columns['time'] = 'TEXT'
        self.columns['day'] = 'TEXT'
        self.columns['name'] = 'TEXT'
        self.columns['venue'] = 'TEXT'

    def get_subject(self,semester,permutation,day,time):
        """"
        Toets
        """
        data = {'semester':semester,
                'permutation':permutation,
                'day':day,
                'time':time}
        self.open()
        result = self.select(cols=['name','venue'],where=data)
        self.close()
        out = ['','']
        if result != {}:
            for i,name in enumerate(result['name']):
                if i==0:
                    out[0] += name
                    out[1] += result['venue'][i]
                else:
                    out[0] += ', ' + name
                    out[1] += ', ' + result['venue'][i]
        return out


