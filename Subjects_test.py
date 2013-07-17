import unittest
import os
import shutil
import Subjects
import sqlite3
import UserOptionsDB
import AllCoursesDB

ROOT = "test_environment/"
class TestGetStudents(unittest.TestCase):
    def setUp(self):
        d = os.path.relpath(ROOT)
        for f in os.listdir(d):
            p = os.path.join(d,f)
            if os.path.isfile(p):
                os.remove(p)
            else:
                shutil.rmtree(p)
                
    def tearDown(self):
        d = os.path.relpath(ROOT)
        for f in os.listdir(d):
            p = os.path.join(d,f)
            if os.path.isfile(p):
                os.remove(p)
            else:
                shutil.rmtree(p)

    

    def test_get_students(self):
        self.options_db = UserOptionsDB.UserOptionsDB(root=ROOT)
        self.courses_db = AllCoursesDB.AllCoursesDB(root=ROOT)
        test_sub = ['sub1','sub2']
        self.options_db.write('subject_names',test_sub)
        old_type = [
                ["sub1","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub1","1","L","2","Tuesday", "12:30:00","13:30:00","Hall"],
                ["sub1","1","P","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","P","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub2","1","P","2","Monday", "12:30:00","13:30:00","Hall"],
                ["sub3","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
                ["sub3","1","L","1","Monday", "12:30:00","13:30:00","Hall"],
            ]
        
        data = convert(old_type)
        self.courses_db.open()
        self.courses_db.insert(data)
        self.courses_db.close()
        subjects = Subjects.get_subjects(root=ROOT)
        self.assertEqual([i.name for i in subjects],test_sub)


def convert(old_type):
    data = {}

    data["name"] = []
    data["semester"] = []
    data["type"] = []
    data["lecture_group"] = []
    data["day"] = []
    data["start_time"] = []
    data["end_time"] = []
    data["venue"] = []

    for row in old_type:
        data["name"].append(row[0])
        data["semester"].append(row[1])
        data["type"].append(row[2])
        data["lecture_group"].append(row[3])
        data["day"].append(row[4])
        data["start_time"].append(row[5])
        data["end_time"].append(row[6])
        data["venue"].append(row[7])
    return data

if __name__=="__main__":
    # check if root exits
    d = os.path.relpath(ROOT)
    if not os.path.exists(d):
        os.makedirs(d)
    unittest.main()
