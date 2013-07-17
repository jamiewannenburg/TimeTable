import unittest
import os
import shutil
import TimeTableDB
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

if __name__=="__main__":
    # check if root exits
    d = os.path.relpath(ROOT)
    if not os.path.exists(d):
        os.makedirs(d)
    unittest.main()
