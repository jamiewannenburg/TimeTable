import sqlite3
import os

class Model:
    """ 
    Object that reads or writes to database. database defined by database_name.
    Attributes:
        name: name of table
        columns: dictionary of key value pairs. Key is column name, value is options.
            .ex {'id':'INTEGER PRIMARY KEY'}
    """
    def __init__(self,root='',database_path='data/',database_name='mydatabase.db'):
        self.root = root
        self.database = root+database_path+database_name
        self.name = 'Model'
        self.columns = {'id': 'INTEGER PRIMARY KEY'}
        self.defaults = {}
        self.order = []
        if not os.path.exists(os.path.join(root,database_path)):
            os.mkdir(os.path.join(root,database_path))

    def make_table(self):
        sql = "CREATE TABLE %s"% self.name
        if self.columns == {}:
            return False
        self.length = len(self.columns)
        sql += "("
        for i,key in enumerate(self.columns):
            if i==0:
                sql += "%s %s"%(key, self.columns[key])
            else:
                sql += ", %s %s"%(key, self.columns[key])
            try:
                sql += " DEFAULT "+str(self.defaults[key])
            except KeyError:
                sql += ""
            self.order.append(key)
        sql += ")"
        sql += ";"
        #print sql
        #try:
        self.cursor.execute(sql)
        self.connection.commit()
        #except sqlite3.OperationalError:
        #    self.cursor.execute("DROP TABLE " + self.name + ";")
        #    self.cursor.execute(sql)
        #    self.connection.commit()

    def open(self):
        """ 
        Open a connection to your database table, and defines cursor.
        Creates tables if they don't exist yet and adds new column names and removes
        unused ones. Returns bool of whether it worked.
        """
        self.connection = sqlite3.connect(self.database) # or use :memory: to put it in RAM
        self.cursor = self.connection.cursor()

        # check if table is the same properties as attributes
        create_table = True
        self.cursor.execute("SELECT * FROM sqlite_master WHERE type='table';")
        results = self.cursor.fetchall()
        tables = []
        for result in results:
            tables.append(result[1])
        if tables:
            if self.name in tables:
                self.cursor.execute("SELECT * FROM " + self.name + ";")
                self.cursor.fetchone()
                props = self.cursor.description
                columns = [i[0] for i in props]
                if len((set(columns)&set(self.columns))) != len(columns):
                    self.cursor.execute("DROP TABLE " + self.name + ";")
                    #self.connection.commit()
                else:
                    for col in columns:
                        self.order.append(col)
                    create_table = False
            

        if create_table:
            self.make_table()
        return True

    def close(self):
        
        self.cursor.close()
        self.connection.close()

    def insert(self,params):
        """ 
        Insert key value pairs (params) into table, where key is a column name. 
        Value can be a iterable where all the values have the same size.
        Return success bool.
        """
        first = True
        inserts = []
        column_names = ""
        qm = ""
        for key in params:
            if not isinstance(params[key],(list,tuple)):
                params[key]=[params[key]]
            if first:
                column_names += str(key)
                qm += "?"
                for value in params[key]:
                    inserts.append([value])
                first = False
            else:
                column_names += "," + str(key)
                qm += ",?"
                for i,value in enumerate(params[key]):
                    inserts[i].append(value)
        
        sql = "INSERT INTO %s(%s) VALUES (%s)"%(self.name,column_names,qm)
        #print sql
        #print inserts
        self.cursor.executemany(sql,inserts)
        self.connection.commit()
        return True

    def update(self,where,params):
        """
        Returns number of rows updated. 
        where: dict of col name and value. WHERE key = value
        params: key value pairs of column and value
        """
        where_str = ""
        set_str = ""
        sql_vars = []

        first = True
        for key in params:
            if key in self.columns:
                if first:
                    set_str += str(key) + "=?"
                    sql_vars.append(params[key])
                    first = False
                else:
                    set_str += ", " + str(key) + "=?"
                    sql_vars.append(params[key])
                
        first = True
        for key in where:
            if key in self.columns:
                if first:
                    where_str += str(key) + "=?"
                    sql_vars.append(where[key])
                    first = False
                else:
                    where_str += " AND " + str(key) + "=?"
                    sql_vars.append(where[key])
        
        sql = "UPDATE %s SET %s WHERE %s"%(self.name, set_str,where_str )
        #print sql
        #print sql_vars
        self.cursor.execute(sql,sql_vars)
        self.connection.commit()
        return self.cursor.rowcount

    def select(self,where={},cols=[],distinct=False,order=''):
        """
        Returns rows matching query.
        where: if empty return all
        """
        sql = ""
        if cols==[]:
            cols = self.order
        # throw out cols that are not in order
        new_cols = []
        for col in cols:
            if col in self.order:
                new_cols.append(col)

        cols = new_cols
        sql += "SELECT "
        if distinct:
            sql += "DISTINCT "
        first = True
        for col in cols:
            if first:
                sql += str(col)
                first = False
            else:
                sql += ", "+str(col)
        sql += " FROM %s"%self.name
        sql_vars=[]
        if where != {}: 
            sql += " WHERE "
            first = True
            for key in where:
                if first:
                    sql += str(key) + "=?"
                    sql_vars.append(where[key])
                    first = False
                else:
                    sql += " AND " + str(key) + "=?"
                    sql_vars.append(where[key])
        if order != "":
            sql += " ORDER BY "+str(order)
        #print sql
        self.cursor.execute(sql,sql_vars)
        result = self.cursor.fetchall()
        out = {}
        for row in result:
            for i,col in enumerate(cols):
                try:
                    out[col].append(row[i])
                except KeyError:
                    out[col] = [row[i]]

        return out
    
