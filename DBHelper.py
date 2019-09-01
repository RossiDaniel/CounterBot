import sqlite3
from datetime import timedelta, datetime, tzinfo
from secret import DB_NAME
import utility

class DBHelper:
    def __init__(self, dbname=DB_NAME):
        self.dbname = dbname

    def delete_id(self,table, id):
        stmt = "DELETE FROM "+str(table)+" WHERE id = (?)"
        args = (id, )
        self.get_result(stmt,args)

    def select_idchat(self,table,idchat):
        stmt = "SELECT * FROM "+str(table)+" WHERE idchat = ?"
        args = (idchat, )
        return self.get_result(stmt,args,True)

    def insert_idchat(self,table,attribute,args):
        stmt = "INSERT INTO "+str(table)+" "+utility.concat(attribute)+" VALUES "+utility.concat(['?' for a in args])
        self.get_result(stmt,args)

    def update_time(self,table,id,hours):
        stmt = "UPDATE "+str(table)+" SET stop = ? WHERE id = ?"
        args = (hours,id, )
        self.get_result(stmt,args)

    def update_hours(self,idchat,hours):
        stmt = "UPDATE account SET sumhours = sumhours + ? WHERE idchat = ?"
        args = (hours,idchat, )
        self.get_result(stmt,args)

    def get_result(self,stmt,args = (),result = False):
        conn = sqlite3.connect(self.dbname)
        if result:
            result = [x for x in conn.execute(stmt,args)]
            self.close(conn)
            return result
        else:
            conn.execute(stmt,args)
            self.close(conn)

    def close(self,conn):
        conn.commit()
        conn.close()
