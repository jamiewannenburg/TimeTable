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

    def save(self,time_tables):
        """
        """
        data = {}
        for col in self.columns:
            if col != 'id':
                data[col] = []
        sem1_count = 0
        sem2_count = 0
        for time_table in time_tables:
            #divide permutations into semesters
            if time_table.semester == 1:
                count = sem1_count
                sem1_count +=1
            else:
                count = sem2_count
                sem2_count +=1
                
            for slot in time_table.slots:
                data['permutation'].append(count)
                data['semester'].append(time_table.semester)
                data['name'].append(slot.subject)
                data['venue'].append(slot.venue)
                data['day'].append(slot.day)
                data['time'].append(slot.time)
        
        self.open()
        self.cursor.execute("DROP TABLE " + self.name + ";")
        self.make_table()
        #print data
        if data!={}:
            self.insert(data)
        self.close()

