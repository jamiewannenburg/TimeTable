import unittest
import os
import shutil
import UserOptionsDB
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

    def test_write(self):
        test_var = 'students'
        db = UserOptionsDB.UserOptionsDB(root=ROOT)
        db.write('test_var',test_var)
        with sqlite3.connect(ROOT+'data/mydatabase.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM user_options;")
            result = c.fetchall()
            #print result
            self.assertTrue('test_var' in result[0])
            self.assertTrue(repr('students') in result[0])

    def test_write_update(self):
        test_var = 'students'
        db = UserOptionsDB.UserOptionsDB(root=ROOT)
        db.write('test_var',test_var)
        test_var = 'test'
        db.write('test_var',test_var)
        with sqlite3.connect(ROOT+'data/mydatabase.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM user_options;")
            result = c.fetchall()
            self.assertTrue('test_var' in result[0])
            self.assertTrue(repr('test') in result[0])

    def test_read(self):
        test_var = 'students'
        db = UserOptionsDB.UserOptionsDB(root=ROOT)
        db.write('test_var',test_var)
        result = db.read('test_var')
        self.assertEqual(result,test_var)

    def test_read_empty(self):
        db = UserOptionsDB.UserOptionsDB(root=ROOT)
        result = db.read('test_var')
        self.assertEqual(result,None)

    def test_read_list(self):
        test_var = ['students','other']
        db = UserOptionsDB.UserOptionsDB(root=ROOT)
        db.write('test_var',test_var)
        result = db.read('test_var')
        self.assertEqual(result,test_var)

    def test_read_dict(self):
        test_var = {'students':2,'other':6}
        db = UserOptionsDB.UserOptionsDB(root=ROOT)
        db.write('test_var',test_var)
        result = db.read('test_var')
        self.assertEqual(result,test_var)

if __name__=="__main__":
    # check if root exits
    d = os.path.relpath(ROOT)
    if not os.path.exists(d):
        os.makedirs(d)
    unittest.main()

