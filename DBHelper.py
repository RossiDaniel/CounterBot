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
        strelapsed_time = "Durata totale: "+self.str_time(result[0][2])
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
            eltime,streltime = self.difference_turno(idchat)
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
    
    def difference_turno(self,idchat):
        result = self.select_idchat('turno',idchat)
        elapsed_time = self.difference_date(result[0][2],result[0][3])
        strelapsed_time = self.str_time(elapsed_time)
        return elapsed_time,strelapsed_time

    def str_time(self,elapsed_time):
        return str(elapsed_time/60)+" ore, "+str(elapsed_time%60)+" minuti"

    def difference_date(self,date1,date2):
        strstart = str(date1).split('-')
        strstop = str(date2).split('-')

        hourstart=str(strstart[0]).split(':')
        datestart=[int(x) for x in str(strstart[1]).split('/')]

        hourstop=str(strstop[0]).split(':')
        datestop=[int(x) for x in str(strstop[1]).split('/')]
        
        difference_day = datetime(datestart[0],datestart[2],datestart[1]) - datetime(datestop[0],datestop[2],datestop[1])

        start = int(hourstart[0])*60 + int(hourstart[1])
        stop = int(hourstop[0])*60 + int(hourstop[1]) + difference_day.days*1440

        elapsed_time = stop-start
        return elapsed_time
    
    def day_hour(self,idchat):
        result = self.select_idchat('data',idchat)
        current_date = now()
        current_data = current_date.split('-')[1]
        
        elapsed_time = 0
        for r in result:
            if r[2].split('-')[1] == current_data:
                elapsed_day = self.difference_date(r[2],r[3])
                elapsed_time += elapsed_day

        return 'Ore lavorate oggi: '+self.str_time(elapsed_time)

def now():
    now = datetime.now()
    minutes = now.hour*60 + now.minute
    best = [(minutes /15)*15,((minutes/15)+1)*15]
    result = min(best, key=lambda x:abs(x-minutes))
    hours = (result / 15) / 4
    minutes = (result - hours*60)
    return str(hours)+":"+str(minutes)+"-"+str(now.year)+"/"+str(now.day)+"/"+str(now.month)

    