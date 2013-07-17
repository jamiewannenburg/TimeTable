from Model import Model
import sqlite3
import os
from bs4 import BeautifulSoup

class AllCoursesDB(Model):
    def __init__(self,root='',database_path='data/',database_name='mydatabase.db'):
        Model.__init__(self,root,database_path,database_name)
        self.name = 'courses'
        self.columns["name"] = 'TEXT'
        self.columns["semester"] = 'TEXT'
        self.columns["type"] = 'TEXT'
        self.columns["lecture_group"] = 'TEXT'
        self.columns["day"] = 'TEXT'
        self.columns["start_time"] = 'TEXT'
        self.columns["end_time"] = 'TEXT'
        self.columns["venue"] = 'TEXT'

    def parse(self,time_table):
        """
        Add html to database.
        """
        soup = BeautifulSoup(time_table)
        
        ##### go through each row in the table #####

        data = {}
        for key in self.columns:
            if key != 'id':
                data[key] = []

        for tr in soup.tbody.find_all('tr'):
            ##### put data of the form d1/d2/d3/d4 in variable seperated = [d1,d2,d3,d4]
            together = tr.td.string
            index = 0;
            seperated = [];
            while index >= 0:
                index1 = together.find( '/', index )
                if index1 == -1:
                    seperated.append(together[index:])
                    index = index1
                else:
                    seperated.append(together[index:index1])
                    index=index1+1
                
            cols = tr.find_all('td')
            
            name = seperated[1]
            type = seperated[4][0]
            lecture_group = int(seperated[2][2:])
            day = cols[2].string
            start_time = cols[3].string
            end_time = cols[4].string
            venue = cols[5].string
            
            if cols[1].string[0] == "S":
                semester = int(cols[1].string[1:])
                data["name"].append(name)
                data["semester"].append(semester)
                data["type"].append(type)
                data["lecture_group"].append(lecture_group)
                data["day"].append(day)
                data["start_time"].append(start_time)
                data["end_time"].append(end_time)
                data["venue"].append(venue)
            elif cols[1].string[0] == "J":
                for sem in range(2):
                    data["name"].append(name)
                    data["semester"].append(sem+1)
                    data["type"].append(type)
                    data["lecture_group"].append(lecture_group)
                    data["day"].append(day)
                    data["start_time"].append(start_time)
                    data["end_time"].append(end_time)
                    data["venue"].append(venue)
        # do database stuff 
        #print data
        self.open()
        self.cursor.execute("DROP TABLE " + self.name + ";")
        #self.connection.commit()
        self.make_table()
        self.insert(data)
        self.close()

    def get_courses(self):
        self.open()
        result = self.select(distinct=True,cols=['name'])
        self.close()
        out=[]
        if result != {}:
            for course in result['name']:
                out.append(course.lower())
        return out
