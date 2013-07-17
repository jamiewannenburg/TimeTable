import unittest
import os
import shutil
import AllCoursesDB
import sqlite3

ROOT = "test_environment/"
class TestFirstRun(unittest.TestCase):
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

    def test_get_courses(self):
        db = AllCoursesDB.AllCoursesDB(root=ROOT)
        data = {}
        data["name"]=['test','test1']
        data["semester"]=[2,3]
        data["type"]=['L','P']
        data["lecture_group"]=[1,2]
        data["venue"]=["venue",'venue2']
        db.open()
        db.insert(data)
        db.close()
        result = db.get_courses()
        self.assertEqual(result,['test','test1'])


if __name__=="__main__":
    # check if root exits
    d = os.path.relpath(ROOT)
    if not os.path.exists(d):
        os.makedirs(d)
    unittest.main()

