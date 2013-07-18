from Model import Model
import sqlite3
import os
from bs4 import BeautifulSoup
from itertools import combinations
from TimeTableDB import TimeTableDB
import datetime
import math

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

    def get_valid_time_tables(self,all_subjects,clashes):
        sem_subjects = {1:[],2:[]}
        self.open()
        types = {}
        for subject in all_subjects:
            types[subject] = []
            self.cursor.execute('select type,semester from '+self.name+' where name=? group by type;',[subject])
            types_result = self.cursor.fetchall()
            sem_subjects[int(types_result[0][1])].append(subject)
            for tr in types_result:
                types[subject].append(tr[0])
        
        data = {}
        data['permutation'] = []
        data['semester'] = []
        data['permutation'] = []
        data['time'] = []
        data['day'] = []
        data['name'] = []
        data['venue'] = []

        count = [0,0]
        for sem in sem_subjects:
            subjects = sem_subjects[sem]
            if subjects != []:
                cols = ""
                tables = ""
                where_clause = ""
                first = True
                table_names = []
                type_map = {}
                params = []
                for i,subject in enumerate(subjects):
                    for l_type in types[subject]:
                        tn = 't' + str(i) + str(l_type)
                        type_map[tn] = [subject,l_type]
                        table_names.append(tn)
                        if first:
                            cols += tn+".lecture_group"
                            tables += self.name+" "+tn
                            where_clause += tn+".name = ? and " + tn + ".type = ?"
                            params.append(subject)
                            params.append(l_type)
                            first = False
                        else:
                            cols += ","+tn+".lecture_group"
                            tables += " join "+self.name+" "+tn
                            where_clause += " and "+tn+".name = ? and " + tn + ".type = ?"
                            params.append(subject)
                            params.append(l_type)

                clashes_str = "sum( case"
                for i,j in combinations(table_names,2):
                    clashes_str += " when "
                    clashes_str += "strftime('%s',"+i+".end_time) - strftime('%s',"+i+".start_time) + "
                    clashes_str += "strftime('%s',"+j+".end_time) - strftime('%s',"+j+".start_time) "
                    clashes_str += "> (select max( "
                    clashes_str += "abs( strftime('%s',"+i+".end_time) - strftime('%s',"+j+".start_time) ),"
                    clashes_str += "abs( strftime('%s',"+j+".end_time) - strftime('%s',"+i+".start_time) )"
                    clashes_str += " )) "
                    clashes_str += "and "+j+".day = "+i+".day then 1"

                clashes_str += " else 0 end )"
                
                sql='select '+ cols +', '+ clashes_str + ' from ' + tables + ' where ' + where_clause + ' group by ' + cols + ';'
                #print sql
                
                self.cursor.execute(sql,params)
                clashes_perms = self.cursor.fetchall()
                
                for perm,clashes_perm in enumerate(clashes_perms):
                    count[sem-1] += 1
                    clash_num = clashes_perm[len(table_names)]
                    if clash_num/len(subjects) <= clashes:
                        for i,tn in enumerate(table_names):
                            subject, l_type = type_map[tn]
                            group = clashes_perm[i]
                            results = self.select(cols=['start_time','end_time','day','venue'],
                                    where={'type':l_type,'name':subject,'lecture_group':group})
                            for i,venue in enumerate(results['venue']):
                                start_time = datetime.datetime.strptime(results['start_time'][i],'%H:%M:%S')
                                end_time =datetime.datetime.strptime(results['end_time'][i],'%H:%M:%S')
                                diff = end_time-start_time
                                for j in xrange(int(math.ceil(float(diff.seconds)/3600.))):
                                    new_time = start_time+datetime.timedelta(hours=j)
                                    data['permutation'].append(perm)
                                    data['semester'].append(sem)
                                    data['name'].append(subject)
                                    data['venue'].append(venue)
                                    data['day'].append(results['day'][i])
                                    data['time'].append( new_time.strftime('%H:%M:%S') )

        self.close()

        db = TimeTableDB()
        db.open()
        db.cursor.execute("DROP TABLE IF EXISTS " + db.name + ";")
        #self.connection.commit()
        db.make_table()
        db.insert(data)
        db.close()

        return count

