import Subjects

class TimeTable:
    def __init__(self,semester):
        self.semester = semester
        self.clashes = 0
        self.slots = []
        
    def add_slot(self,new_slot):
        for slot in self.slots:
            if (str(new_slot.time) == str(slot.time))&(str(new_slot.day) == str(slot.day)):
                self.clashes += 1
        self.slots.append(new_slot)
        return True
            
        
class Slot(TimeTable):
    def __init__(self,subject,day,time,venue):
        self.subject = subject
        self.day = day
        self.time = time
        self.venue = venue

def add_time_tables(tt1,tt2):
    """
        Generte a new time table by combining two given time tables.
    """
    
    if str(tt1.semester) != str(tt2.semester):
        tt = TimeTable(1)
        tt.clashes = float("inf")
        return tt
        
    tt = TimeTable(tt1.semester)
    for slot in tt1.slots:
        tt.add_slot(slot)
    for slot in tt2.slots:
        tt.add_slot(slot)
        
    return tt


def get_valid_time_tables(subjects,clashes):
    """
        Generate a list of time tables from subjects that have less clashes than 
        specified in clashes.
    """
    clashes = int(clashes)
    i=0
    fringe = subjects[i].get_time_tables()
    i = i + 1
    
    
    while i < len(subjects) :
        # first proon fringe to only valad
        new_fringe = []
        for time_table in fringe:
            #print 'clashes',time_table.clashes
            if time_table.clashes <= clashes:
                new_fringe.append(time_table)
                
        
        # if there are no time tables in fringe that meet the condition you are done
        #print 'fringe',new_fringe
        if len(new_fringe)==0:
            print 'no time tables'
            return []
            
        # expand fringe to include slots from the next subject
        fringe = []
        new_time_tables = subjects[i].get_time_tables()
        for time_table in new_fringe:
            for new_time_table in new_time_tables:
                fringe.append(add_time_tables(time_table,new_time_table))
            
        i = i + 1
    
    valid_tt = []
    for time_table in fringe:
        if time_table.clashes <= clashes:
            
            valid_tt.append(time_table)
    return valid_tt
    
    