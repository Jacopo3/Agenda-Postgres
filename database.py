"""
CREATE TABLE tasks (
    id bigserial not null primary key,
    titolo text not null,
    descrizione text,
    fatto integer,
    data date,
    giorno_sett_rp integer,
    annua_rp date
)


SELECT * 
FROM tasks
WHERE to_char(annua_rp, 'YYYY-MM-DD') LIKE '%-02-05';

"""
"""
insert into tasks (
    titolo,
    descrizione,
    fatto,
    data
) values (
    'Ciao',
    'prima tasks',
    0,
    date '2022-02-08'
)

insert into tasks (
    titolo,
    descrizione,
    fatto,
    annua_rp
) values (
    'Ciao',
    'prima tasks',
    1,
    date '2020-02-05'
)

insert into tasks (
    titolo,
    descrizione,
    giorno_sett_rp
) values (
    'Ciao',
    'prima tasks',
    6
)


"""
import psycopg2
import psycopg2.extras
import datetime

def tasks():
    connection = psycopg2.connect(user="",
                                password="",
                                host="127.0.0.1",
                                port="5432",
                                database="agenda")
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return connection, cur

def task_clo(cur, connection):
    try:
        cur.close()
        connection.close()
    except:
        print("no bro no database non chiuso")
        
def leggi(cur, data_str = None):
    data = data_str
    if data_str == None or data_str == "":
        data_str = datetime.date.today()
        data = datetime.date.today()
    elif type(data_str) == str and data_str != "": 
        data = data_str.split("-")
        data = datetime.date(int(data[0]), int(data[1]), int(data[2]))
    
    data_fine = data + datetime.timedelta(days= 7)
    
    data_str_annua_rp = str(data_str)[4:]
    
    cur.execute(f"SELECT * FROM tasks WHERE to_char(annua_rp, 'YYYY-MM-DD') LIKE '%{data_str_annua_rp}' or giorno_sett_rp = {data.weekday()}or data BETWEEN date'{data_str}' AND date'{str(data_fine)}' order by annua_rp, giorno_sett_rp, data;")
    if __name__ == "__main__":
        for row in cur.fetchall():
            print(row)
    return cur.fetchall()

def leggi_id(cur, id):
    id = int(id)
    cur.execute(f"SELECT * FROM tasks WHERE id = {id}")
    return cur.fetchall()

def scrivi(conn, cur,array):
    ar = ["NULL" if i is None else i for i in array ]  
    if ar[2] != "NULL" and ar[4] != "NULL":
        cur.execute(f"INSERT INTO tasks (titolo, descrizione, data, giorno_sett_rp, annua_rp) VALUES ('{ar[0]}', '{ar[1]}', DATE'{ar[2]}', {ar[3]}, DATE'{ar[4]}')")
    elif ar[2] == "NULL" and ar[4] != "NULL":
        cur.execute(f"INSERT INTO tasks (titolo, descrizione, data, giorno_sett_rp, annua_rp) VALUES ('{ar[0]}', '{ar[1]}', {ar[2]}, {ar[3]}, DATE'{ar[4]}')")
    elif ar[4] == "NULL" and ar[2] != "NULL":
        cur.execute(f"INSERT INTO tasks (titolo, descrizione, data, giorno_sett_rp, annua_rp) VALUES ('{ar[0]}', '{ar[1]}', DATE'{ar[2]}', {ar[3]}, {ar[4]})")
    else: 
        cur.execute(f"INSERT INTO tasks (titolo, descrizione, data, giorno_sett_rp, annua_rp) VALUES ('{ar[0]}', '{ar[1]}', {ar[2]}, {ar[3]}, {ar[4]})")
    conn.commit()

def fatto_db(conn, cur, id_task, value):
    id_task = int(id_task)
    if value == None:
        value = 0
        cur.execute(f"UPDATE tasks SET fatto = {value} WHERE id = {id_task}")
    elif value == "on":
        value = 1
        cur.execute(f"UPDATE tasks SET fatto = {value} WHERE id = {id_task}")
    conn.commit()

def modifica_task(conn, cur, id_task, array):
    where = f"WHERE id = {id_task}"
    ar = ["NULL" if i is None else i for i in array ]  
    if ar[2] != "NULL" and ar[4] != "NULL":
        cur.execute(f"UPDATE tasks SET titolo = '{ar[0]}', descrizione = '{ar[1]}', data = DATE'{ar[2]}', giorno_sett_rp = {ar[3]}, annua_rp = DATE'{ar[4]}' {where}")
    elif ar[2] == "NULL" and ar[4] != "NULL":
        cur.execute(f"UPDATE tasks SET titolo = '{ar[0]}', descrizione = '{ar[1]}', data = {ar[2]}, giorno_sett_rp = {ar[3]}, annua_rp = DATE'{ar[4]}' {where}")
    elif ar[4] == "NULL" and ar[2] != "NULL":
        cur.execute(f"UPDATE tasks SET titolo = '{ar[0]}', descrizione = '{ar[1]}', data = DATE'{ar[2]}', giorno_sett_rp = {ar[3]}, annua_rp = {ar[4]} {where}")
    else: 
        cur.execute(f"UPDATE tasks SET titolo = '{ar[0]}', descrizione = '{ar[1]}', data = {ar[2]}, giorno_sett_rp = {ar[3]}, annua_rp = {ar[4]} {where}")
    conn.commit()
if __name__ == "__main__":
    conn, cur = tasks()
    leggi(cur, "2022-02-05")
    scrivi(conn,cur, ["Palestra", "Braccia", "2022-02-10", None, None])
    task_clo(cur, conn)
