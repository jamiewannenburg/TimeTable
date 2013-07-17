from datetime import datetime 
from datetime import timedelta
import TimeTables
import AllCoursesDB
import UserOptionsDB

class Subject:
    def __init__(self,name,semester):
        self.name = name
        self.semester = int(semester)
        self.lecture_types = [] # a list of LectureType's
        
    def add_time(self,args):
        """
            Takes as input [type ,group, day ,start_time ,end_time ,venue]
            Checks whether there is already a lecture type of type type. (That is a sentence) 
            Creates a new one if not, and calls a similar function on it.
        """
        
        for type in self.lecture_types:
            if type.type == args[0]:
                type.add_time(args[1:])
                return True
        type = LectureType(args[0])
        type.add_time(args[1:])
        self.lecture_types.append(type)
        return True
        
    def get_time_tables(self):
        # save options in slots
        slots = []
        sizes = []
        for i,type in enumerate(self.lecture_types):
            slots.append([])
            sizes.append(len(type.groups))
            for j,group in enumerate(type.groups):
                slots[i].append([])
                for time in group.times:
                    slots[i][j].append(TimeTables.Slot(self.name,time.day,time.time,time.venue))
                    
        # create permutations (gaussian product) 
        permutations=[[]]
        pools = []
        for i in sizes:
            pools.append(range(i))
        for pool in pools:
            permutations = [x+[y] for x in permutations for y in pool]
                
        tts = []
        
        for perm in permutations:
            tt = TimeTables.TimeTable(self.semester)
            for i,group_no in enumerate(perm):
                for slot in slots[i][group_no]:
                    tt.add_slot(slot)
            tts.append(tt)
                    
        return tts
    
class LectureType(Subject):
    def __init__(self,type):
        self.type = type
        self.groups = []
        
    def add_time(self,args):
        """
            Takes as input [group ,start_time ,end_time ,venue]
            Checks whether there is already a group of number 'Group'. 
            Creates a new one if not, and calls a similar function on it.
        """
        
        for group in self.groups:
            if group.number == args[0]:
                group.add_time(args[1:])
                return True
        group = Group(args[0])
        group.add_time(args[1:])
        self.groups.append(group)
        return True
        
class Group(LectureType):
    def __init__(self,number):
        self.number = number
        self.times = []
        
    def add_time(self,args):
        """
        Takes as input [start_time ,end_time ,venue]
        This function assumes all lectures are in blocks of one hour.
        If the duration is more than an hour it creates two times.
        """
        
        start_time = datetime.strptime(args[1], "%H:%M:%S")
        end_time = datetime.strptime(args[2], "%H:%M:%S")
        start_hour = start_time.strftime("%H")
        end_hour = end_time.strftime("%H")
        duration = (int(end_hour) - int(start_hour))
        
        for i in range(duration):
            time = Time(args[0],datetime.strftime(start_time + timedelta(hours=i), "%H:%M:%S"),args[3])
            self.times.append(time)
        return True
    
class Time(Group):
    def __init__(self,day,time,venue):
        self.day = day
        self.time = time
        self.venue = venue
        
# 0 name ,1 semester ,2 type ,3 group ,4 day,5 start_time ,6 end_time ,7 venue

def get_subjects(root=''):
    # get data from databases
    courses_db = AllCoursesDB.AllCoursesDB(root=root)
    user_options = UserOptionsDB.UserOptionsDB(root=root)
    names = user_options.read('subject_names')
    courses_db.open()
    out = []
    done = [[],[]]
    for name in names:
        course = courses_db.select(where={'name':name})
        for i,course_name in enumerate(course['name']):
            if (name in done[0]) & (course['semester'][i] in done[1]) :
                for subject in out:
                    if (name == str(subject.name)) & (course['semester'][i] == str(subject.semester)):
                        subject.add_time([ course["type"][i],
                            course["lecture_group"][i],
                            course["day"][i],
                            course["start_time"][i],
                            course["end_time"][i],
                            course["venue"][i] ])
            else:
                subject = Subject(name,course['semester'][i])
                subject.add_time([ course["type"][i],
                    course["lecture_group"][i],
                    course["day"][i],
                    course["start_time"][i],
                    course["end_time"][i],
                    course["venue"][i] ])
                out.append(subject)
                done[0].append(name)
                done[1].append(course['semester'][i])

    courses_db.close()
                
    return out
                
                
