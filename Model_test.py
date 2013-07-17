import unittest
import os
import shutil
import Model
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

    def test_make_data(self):
        m = Model.Model(root=ROOT)
        m.open()
        m.close()
        r = os.path.relpath(ROOT)
        p = os.path.join(r,"data")
        self.assertTrue(os.path.exists(p))

    def test_make_database(self):
        m = Model.Model(root=ROOT,database_name="mydb.db")
        m.name = 'test_table'
        m.open()
        m.close()
        r = os.path.relpath(ROOT)
        p = os.path.join(r,"data","mydb.db")
        self.assertTrue(os.path.exists(p))

    
    def test_make_table(self):
        m = Model.Model(root=ROOT,database_path='',database_name="mydb.db")
        m.name = 'test_table'
        m.columns = {'col1':'INTEGER'}
        m.open()
        m.close()
        
        conn = sqlite3.connect(ROOT+'mydb.db')
        c = conn.cursor()
        c.execute("SELECT * FROM sqlite_master WHERE type='table';")
        result = c.fetchone()
        c.close()
        conn.close()
        self.assertTrue('test_table' in result)

    def test_make_column(self):
        m = Model.Model(root=ROOT,database_path='',database_name="mydb.db")
        m.name = 'test_table'
        m.columns = {'col1':'INTEGER'}
        m.open()
        m.close()
        with sqlite3.connect(ROOT+'mydb.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM test_table;")
            c.fetchall()
            self.assertTrue('col1' in c.description[0])

    def test_insert(self):
        m = Model.Model(root=ROOT,database_path='',database_name="mydb.db")
        m.name = 'test_table'
        m.columns = {'col1':'INTEGER','col2': 'TEXT'}
        m.open()
        m.insert({'col1': 2,'col2':'Test'})
        m.close()
        with sqlite3.connect(ROOT+'mydb.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM test_table;")
            result = c.fetchall()
            self.assertTrue(2 in result[0])
            self.assertTrue('Test' in result[0])

    def test_insert_many(self):
        m = Model.Model(root=ROOT,database_path='',database_name="mydb.db")
        m.name = 'test_table'
        m.columns = {'col1':'INTEGER','col2': 'TEXT'}
        m.open()
        m.insert({'col1': (2,3),'col2':('Test1','Test2')})
        m.close()
        with sqlite3.connect(ROOT+'mydb.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM test_table;")
            result = c.fetchall()
            self.assertTrue(2 in result[0])
            self.assertTrue('Test1' in result[0])
            self.assertTrue(3 in result[1])
            self.assertTrue('Test2' in result[1])

    def test_default(self):
        m = Model.Model(root=ROOT,database_path='',database_name="mydb.db")
        m.name = 'test_table'
        m.columns = {'col1':'INTEGER','col2': 'TEXT'}
        m.defaults = {'col1':0}
        m.open()
        m.insert({'col2':'Test'})
        m.close()
        with sqlite3.connect(ROOT+'mydb.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM test_table;")
            result = c.fetchall()
            self.assertTrue(0 in result[0])
    
    def test_update(self):
        m = Model.Model(root=ROOT,database_path='',database_name="mydb.db")
        m.name = 'test_table'
        m.columns['col1']='INTEGER'
        m.columns['col2']='TEXT'
        m.defaults = {'col1':0}
        m.open()
        m.insert({'col1': 2})
        rows = m.update({'id': 1},{'col1':3})
        m.close()
        with sqlite3.connect(ROOT+'mydb.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM test_table;")
            result = c.fetchall()
            #print result
            self.assertTrue(rows == 1)
            self.assertTrue(3 in result[0])

    def test_select_all(self):
        m = Model.Model(root=ROOT,database_path='',database_name="mydb.db")
        m.name = 'test_table'
        m.columns = {'col1': 'INTEGER','col2': 'TEXT'}
        m.open()
        m.insert({'col1': 2,'col2': 'Test'})
        result = m.select()
        m.close()
        self.assertTrue(2 == result['col1'][0])
        self.assertTrue('Test' in result['col2'][0])

    def test_select_cols(self):
        m = Model.Model(root=ROOT,database_path='',database_name="mydb.db")
        m.name = 'test_table'
        m.columns = {'col1': 'INTEGER','col2': 'TEXT','col3': 'REAL'}
        m.open()
        m.insert({'col1': 2,'col2': 'Test','col3': 5.3})
        result = m.select(cols=['col1','col2'])
        m.close()
        self.assertTrue(2 == result['col1'][0])
        self.assertRaises(KeyError,lambda: result['col3'])

    def test_select_where(self):
        m = Model.Model(root=ROOT,database_path='',database_name="mydb.db")
        m.name = 'test_table'
        m.columns = {'col1': 'INTEGER','col2': 'TEXT'}
        m.open()
        m.insert({'col1': (2,3),'col2': ('Test1','Test2')})
        result = m.select(where={'col1': 3})
        m.close()
        self.assertTrue(3 == result['col1'][0])

    def test_select_distinct(self):
        m = Model.Model(root=ROOT,database_path='',database_name="mydb.db")
        m.name = 'test_table'
        m.columns = {'col1': 'INTEGER','col2': 'TEXT'}
        m.open()
        m.insert({'col1': (2,2),'col2': ('Test1','Test2')})
        result = m.select(cols=['col1'],distinct=True)
        m.close()
        self.assertTrue(1 == len(result['col1']))
        self.assertTrue(2 == result['col1'][0])

    def test_select_onder(self):
        m = Model.Model(root=ROOT,database_path='',database_name="mydb.db")
        m.name = 'test_table'
        m.columns = {'col1': 'INTEGER','col2': 'TEXT'}
        m.open()
        m.insert({'col1': (2,1),'col2': ('Test1','Test2')})
        result = m.select(cols=['col1'],order='col2')
        m.close()
        self.assertTrue(2 == result['col1'][0])
        self.assertTrue(1 == result['col1'][1])

class TestGeneral(unittest.TestCase):
    def setUp(self):
        self.m = Model.Model(root=ROOT,database_path='',database_name="mydb.db")
        self.m.name = 'test_table'
        self.m.columns = {'id':'INTEGER PRIMARY KEY','col1': 'INTEGER','col2': 'TEXT'}
        self.m.open()
        self.m.insert({'col1': (4,3,2,1),'col2': ('Test1','Test2','Test3','Test4')})
        self.m.close()
                
    def tearDown(self):
        d = os.path.relpath(ROOT)
        for f in os.listdir(d):
            p = os.path.join(d,f)
            if os.path.isfile(p):
                os.remove(p)
            else:
                shutil.rmtree(p)

    def test_insert(self):
        self.m.open()
        self.m.insert({'col1':5,'col2':'Test'})
        self.m.close()
        with sqlite3.connect(ROOT+'mydb.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM test_table;")
            result = c.fetchall()
            self.assertTrue(5 in result[4])
            self.assertTrue('Test' in result[4])

    def test_new_config(self):
        self.m.columns = {'col1':'INTEGER','col2':'TEXT'}
        self.m.open()
        self.m.insert({'col1':5,'col2':'Test'})
        self.m.close()
        with sqlite3.connect(ROOT+'mydb.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM test_table;")
            result = c.fetchall()
            self.assertTrue(5 in result[0])
            self.assertTrue('Test' in result[0])


if __name__=="__main__":
    # check if root exits
    d = os.path.relpath(ROOT)
    if not os.path.exists(d):
        os.makedirs(d)
    unittest.main()

