import sqlite3
from datetime import timedelta, datetime, tzinfo

class DBHelper:
    def __init__(self, dbname="counterbot.db"):
        self.dbname = dbname

    def start(self,idchat):
        result = self.select_idchat('account',idchat)
        
        if len(result) == 0:
            stmt = "INSERT INTO account (idchat) VALUES (?)"
            args = (idchat,)
            conn = sqlite3.connect(self.dbname)
            conn.execute(stmt, args)
            conn.commit()
            conn.close()
            result = self.select_idchat('account',idchat)
        return result

    def total_hour(self,idchat):
        result = self.select_idchat('account',idchat)
        result[0][2]
        strelapsed_time = "Durata totale: "+str(result[0][2]/60)+" ore, "+str(result[0][2]%60)+" minuti"
        return strelapsed_time


    def shift_press(self, idchat):
        current_d = now()
        result = self.select_idchat('turno',idchat)

        if len(result) == 0:
            stmt = "INSERT INTO turno (idchat,start) VALUES (?,?)"
            args = (idchat,current_d )
            conn = sqlite3.connect(self.dbname)
            conn.execute(stmt, args)
            conn.commit()
            conn.close()
            return "Inizio: "+str(current_d)
        else:
            stmt = "UPDATE turno SET stop = ? WHERE idchat = ?"
            args = (current_d,idchat )
            conn = sqlite3.connect(self.dbname)
            conn.execute(stmt, args)
            conn.commit()
            conn.close()
            eltime,streltime = self.difference(idchat)
            self.add_hours(eltime,idchat)
            self.delete_idchat('turno',idchat)
            return "Fine: "+str(current_d)+"\n"+"Durata: "+streltime


    def delete_idchat(self,table, idchat):
        stmt = "DELETE FROM "+str(table)+" WHERE idchat = (?)"
        args = (idchat, )
        conn = sqlite3.connect(self.dbname)
        conn.execute(stmt, args)
        conn.commit()
        conn.close()

    def add_hours(self,hours,idchat):
        stmt = "UPDATE account SET sumhours = sumhours + ? WHERE idchat = ?"
        args = (hours,idchat, )
        conn = sqlite3.connect(self.dbname)
        conn.execute(stmt, args)
        conn.commit()
        conn.close()
        

    def select_idchat(self,table,idchat):
        stmt = "SELECT * FROM "+str(table)+" WHERE idchat = ?"
        args = (idchat, )
        conn = sqlite3.connect(self.dbname)
        result = [x for x in conn.execute(stmt,args)]
        conn.close()
        return result
    
    def difference(self,idchat):
        result = self.select_idchat('turno',idchat)
        strstart = str(result[0][2]).split('-')
        strstop = str(result[0][3]).split('-')

        hourstart=str(strstart[0]).split(':')
        datestart=[int(x) for x in str(strstart[1]).split('/')]

        hourstop=str(strstop[0]).split(':')
        datestop=[int(x) for x in str(strstop[1]).split('/')]
        
        difference_day = datetime(datestart[0],datestart[2],datestart[1]) - datetime(datestop[0],datestop[2],datestop[1])


        start = int(hourstart[0])*60 + int(hourstart[1])
        stop = int(hourstop[0])*60 + int(hourstop[1]) + difference_day.days*1440

        elapsed_time = stop-start
        strelapsed_time = str(elapsed_time/60)+" ore, "+str(elapsed_time%60)+" minuti"
        return elapsed_time,strelapsed_time
    
    def day_hour(self,idchat):
        return 'Ore lavorate oggi: '

def now():
    now = datetime.now()
    minutes = now.hour*60 + now.minute
    best = [(minutes /15)*15,((minutes/15)+1)*15]
    result = min(best, key=lambda x:abs(x-minutes))
    hours = (result / 15) / 4
    minutes = (result - hours*60)
    return str(hours)+":"+str(minutes)+"-"+str(now.year)+"/"+str(now.day)+"/"+str(now.month)

    