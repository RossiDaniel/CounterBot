import sqlite3

conn = sqlite3.connect('counterbot.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS account
             (id integer primary key, idchat varchar unique, sumhours integer default 0)''')

c.execute('''CREATE TABLE IF NOT EXISTS turno
             (id integer primary key, idchat varchar unique REFERENCES account(idchat), start text NULL, stop text NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS data
             (id integer primary key, idchat varchar REFERENCES account(idchat), start text NULL, stop text NULL)''')
c.execute('''CREATE TRIGGER IF NOT EXISTS archive AFTER DELETE 
            ON turno
            BEGIN
            INSERT INTO data(idchat, start,stop) VALUES (old.idchat, old.start,old.stop);
            END;''')