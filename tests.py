# This is the file where I keep all my test cases.


class TestCase:
    size = 0
    def __init__(self,function,arguments,result,description=""):
        self.function = function
        self.description = description
        self.arguments = arguments
        self.result = result
        self.number = TestCase.size + 1
        TestCase.size = TestCase.size + 1
        
    def test(self):
        args = self.arguments
        if len(args) == 1 :
            check = self.function(args[0])
            
        elif len(args) == 2 :
            check = self.function(args[0],args[1])
        
        elif len(args) == 3 :
            check = self.function(args[0],args[1],args[2])
        
        elif len(args) == 4 :
            check = self.function(args[0],args[1],args[2],args[3])
        
        elif len(args) == 5 :
            check = self.function(args[0],args[1],args[2],args[3],args[4])
        
        elif len(args) == 6 :
            check = self.function(args[0],args[1],args[2],args[3],args[4],args[5])
        
        else:
            raise Exception("Only functions with less than 7 inputs can be tested")
            
        if check == self.result:
            print self.number, "Pass", self.function.__name__, self.description
        else:
            print self.number, "Fail", self.function.__name__, self.description
            print "Got", check, " instread of ", self.result 
        
    def displayTest(self,input,output=""):
        args = self.arguments
        if args == None :
            check = self.function()
        elif len(args) == 1 :
            check = self.function(args[0])
            
        elif len(args) == 2 :
            check = self.function(args[0],args[1])
        
        elif len(args) == 3 :
            check = self.function(args[0],args[1],args[2])
        
        elif len(args) == 4 :
            check = self.function(args[0],args[1],args[2],args[3])
        
        elif len(args) == 5 :
            check = self.function(args[0],args[1],args[2],args[3],args[4])
        
        elif len(args) == 6 :
            check = self.function(args[0],args[1],args[2],args[3],args[4],args[5])
        
        else:
            raise Exception("Only functions with less than 7 inputs can be tested")
            
        if check == self.result:
            print self.number, "Pass", self.function.__name__, self.description
        else:
            print self.number, "Fail", self.function.__name__, self.description
            print "Got", check, " instread of ", self.result 

# ##### Display Functions #####
# from DisplayFunctions import clear_screen

# description = "Check Functionality"
# TestCase(clear_screen,None,True,description).displayTest("","")

# from DisplayFunctions import yn_input

# description = "Check Yes"
# TestCase(yn_input,("Is this a test","y"),True,description).displayTest("y")

import Subjects
# 0 name ,1 semester ,2 type ,3 group ,4 start_time ,5 end_time ,6 venue
input = ["Monday","12:30:00","13:30:00","Hall"]
description = "check on Group"
TestCase(Subjects.Group(1).add_time,[input],True,description).test()

input = ["Monday","12:30:00","15:30:00","Hall"]
description = "check on Group tree hours"
TestCase(Subjects.Group(1).add_time,[input],True,description).test()

input = ["1","Monday","12:30:00","13:30:00","Hall"]
description = "check on LectureType"
TestCase(Subjects.LectureType("P").add_time,[input],True,description).test()

input = ["P","1","Monday","12:30:00","13:30:00","Hall"]
description = "check on Subject"
TestCase(Subjects.Subject("sub",1).add_time,[input],True,description).test()

def test_names(input):
    subjects = Subjects.get_subjects(input[0],input[1])
    return [subject.name for subject in subjects]
    
input = [
            [
                ["sub1","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub1","1","L","2","Tuesday", "12:30:00","13:30:00","Hall"],
                ["sub1","1","P","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","P","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","P","2","Monday", "12:30:00","13:30:00","Hall"],
                ["sub3","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub3","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
            ],
            ["sub1","sub2"]
        ]
description = "check get_subjects on subject names"
output = ["sub1","sub2"]
TestCase(test_names,[input],output,description).test()

def test_types(input):
    subjects = Subjects.get_subjects(input[0],input[1])
    return [type.type for type in subjects[0].lecture_types]
    
input = [
            [
                ["sub1","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub1","1","L","2","Tuesday", "12:30:00","13:30:00","Hall"],
                ["sub1","1","P","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","P","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","P","2","Monday", "12:30:00","13:30:00","Hall"],
                ["sub3","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub3","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
            ],
            ["sub1","sub2"]
        ]
description = "check get_subjects on lecture_types"
output = ["L","P"]
TestCase(test_types,[input],output,description).test()

def test_groups(input):
    subjects = Subjects.get_subjects(input[0],input[1])
    return [group.number for group in subjects[0].lecture_types[0].groups]
    
input = [
            [
                ["sub1","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub1","1","L","2","Tuesday", "12:30:00","13:30:00","Hall"],
                ["sub1","1","P","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","P","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","P","2","Monday", "12:30:00","13:30:00","Hall"],
                ["sub3","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub3","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
            ],
            ["sub1","sub2"]
        ]
description = "check get_subjects on groups"
output = ["1","2"]
TestCase(test_groups,[input],output,description).test()

def test_times(input):
    subjects = Subjects.get_subjects(input[0],input[1])
    return [time.time for time in subjects[0].lecture_types[0].groups[0].times]
    
input = [
            [
                ["sub1","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub1","1","L","1","Tuesday", "12:30:00","13:30:00","Hall"],
                ["sub1","1","P","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","P","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","P","2","Monday", "12:30:00","13:30:00","Hall"],
                ["sub3","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub3","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
            ],
            ["sub1","sub2"]
        ]
description = "check get_subjects on times"
output = ["12:30:00","12:30:00"]
TestCase(test_times,[input],output,description).test()

def test_days(input):
    subjects = Subjects.get_subjects(input[0],input[1])
    return [time.day for time in subjects[0].lecture_types[0].groups[0].times]
    
input = [
            [
                ["sub1","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub1","1","L","1","Tuesday", "12:30:00","13:30:00","Hall"],
                ["sub1","1","P","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","P","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","P","2","Monday", "12:30:00","13:30:00","Hall"],
                ["sub3","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub3","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
            ],
            ["sub1","sub2"]
        ]
description = "check get_subjects on days"
output = ["Monday","Tuesday"]
TestCase(test_days,[input],output,description).test()

def test_get_time_tables_times(input):
    subjects = Subjects.get_subjects(input[0],input[1])
    time_tables = subjects[0].get_time_tables()
    
    return [slot.time for slot in time_tables[0].slots]
    
input = [
            [
                ["sub1","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub1","1","L","1","Tuesday", "12:30:00","13:30:00","Hall"],
                ["sub1","1","P","1","Friday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","P","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","P","2","Monday", "12:30:00","13:30:00","Hall"],
                ["sub3","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub3","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
            ],
            ["sub1"]
        ]
description = "check get_time_tables on times"
output = ["12:30:00", "12:30:00","12:30:00"]
TestCase(test_get_time_tables_times,[input],output,description).test()

def test_get_time_tables_days(input):
    subjects = Subjects.get_subjects(input[0],input[1])
    time_tables = subjects[0].get_time_tables()
    
    return [slot.day for slot in time_tables[0].slots]
    
input = [
            [
                ["sub1","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub1","1","L","1","Tuesday", "12:30:00","13:30:00","Hall"],
                ["sub1","1","P","1","Friday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","P","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","P","2","Monday", "12:30:00","13:30:00","Hall"],
                ["sub3","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub3","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
            ],
            ["sub1"]
        ]
description = "check get_time_tables on days"
output = ["Monday", "Tuesday","Friday"]
TestCase(test_get_time_tables_days,[input],output,description).test()

def test_get_time_tables_two_groups(input):
    subjects = Subjects.get_subjects(input[0],input[1])
    time_tables = subjects[0].get_time_tables()
    out = [[slot.time for slot in time_tables[0].slots],
    [slot.time for slot in time_tables[1].slots]]
    return out
    
input = [
            [
                ["sub1","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub1","1","L","2","Tuesday", "14:30:00","15:30:00","Hall"],
                ["sub1","1","P","1","Friday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","P","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","P","2","Monday", "12:30:00","13:30:00","Hall"],
                ["sub3","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub3","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
            ],
            ["sub1"]
        ]
description = "check get_time_tables on two groups"
output = [["12:30:00", "12:30:00"],["14:30:00", "12:30:00"]]
TestCase(test_get_time_tables_two_groups,[input],output,description).test()


##### test TimeTables' functions #####
import TimeTables

description = "check"
input = TimeTables.Slot("sub1","Monday","12:30:00","Hall")
time_table = TimeTables.TimeTable(1)
TestCase(time_table.add_slot,[input],True,description).test()

def test_add_block(slot1,slot2):
    time_table = TimeTables.TimeTable(1)
    time_table.add_slot(slot1)
    time_table.add_slot(slot2)
    
    return (time_table.clashes,[slot.time for slot in time_table.slots])
    
description = "check for duplicates"
slot1 = TimeTables.Slot("sub1","Monday","12:30:00","Hall")
slot2 = TimeTables.Slot("sub2","Monday","12:30:00","Hall")
time_table = TimeTables.TimeTable(1)
result = (1,["12:30:00","12:30:00"])
TestCase(test_add_block,[slot1,slot2],result,description).test()


def test_get_valid_time_tables_two_subjects(input):
    subjects = Subjects.get_subjects(input[0],input[1])
    time_tables = TimeTables.get_valid_time_tables(subjects,0)
    out = [slot.time for slot in time_tables[0].slots]
    
    if len(time_tables) != 1:
        print len(time_tables)
        return False
    return out
    
input = [
            [
                ["sub1","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub1","1","P","1","Friday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","L","1","Monday", "13:30:00","14:30:00","Hall"],
                ["sub2","1","P","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","P","2","Monday", "15:30:00","16:30:00","Hall"],
                ["sub3","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub3","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
            ],
            ["sub1","sub2"]
        ]
description = "check get_time_tables on two groups"
output = ["12:30:00", "12:30:00","13:30:00","15:30:00"]
TestCase(test_get_valid_time_tables_two_subjects,[input],output,description).test()






