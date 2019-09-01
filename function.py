import sqlite3
from DBHelper import DBHelper
import utility

def fstart(idchat):
    dbh = DBHelper()
    result = dbh.select_idchat('account',idchat)

    if len(result) == 0:
        dbh.insert_idchat('account',['idchat'],[idchat])
    

def ftot(idchat):
        dbh = DBHelper()
        result = dbh.select_idchat('account',idchat)
        strelapsed_time = "Durata totale: "+utility.str_time(result[0][2])
        return strelapsed_time


def fpunch(idchat):
    current_d = utility.now()
    dbh = DBHelper()
        
    result = dbh.select_idchat('turno',idchat)

    if len(result) == 0:
        dbh.insert_idchat('turno',['idchat','start'],[idchat,current_d])
        return "Inizio: "+str(current_d)
    else:
        dbh.update_time('turno',result[0][0],current_d)
        elapsed_time = utility.difference(result[0][2],current_d)
        dbh.update_hours(idchat,elapsed_time)
        dbh.delete_id('turno',result[0][0])
        return "Fine: "+str(current_d)+"\n"+"Durata: "+utility.str_time(elapsed_time)
    
def fday(idchat):
    dbh = DBHelper()
    result = dbh.select_idchat('data',idchat)
    current_date = utility.now()
    current_data = current_date.split('-')[1]
    
    elapsed_time = 0
    for r in result:
        if r[2].split('-')[1] == current_data:
            elapsed_day = utility.difference(r[2],r[3])
            elapsed_time += elapsed_day

    return 'Ore lavorate oggi: '+utility.str_time(elapsed_time)

def fopt(idchat):
    dbh = DBHelper()
    result = dbh.select_idchat('data',idchat)
    i = 1
    while i < len(result):
        if result[i-1][3] == result[i][2]:
            result[i-1][3] == result[i][3]
            dbh.delete_id('data',result[i][0])
            result.pop(i)
        else:
            i=i+1
    return 'Ottimizzato!'
