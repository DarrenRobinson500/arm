import sqlite3
from datetime import datetime, timedelta

def db(db_str):
    con = sqlite3.connect('data.db')
    c = con.cursor()
    # print(db_str)
    c.execute(db_str)
    output = c.fetchall()
    con.commit()
    con.close()
    return output

def db_create_table():
    db_str = "CREATE TABLE general(name TEXT, variable TEXT, value_text TEXT, value_float FLOAT)"
    db(db_str)

def db_delete_table(table):
    db_str = f"DROP TABLE {table}"
    db(db_str)

def db_update(name, variable, value, variable_type):
    condition = f" WHERE name='{name}' and variable = '{variable}'"
    db_str = f"SELECT * FROM general" + condition
    value_string, value_float = "", 0
    if variable_type == "string": value_string = value
    else: value_float = value
    if value_float is None: value_float = 0

    existing = len(db(db_str))
    if existing == 0:
        db(f"INSERT INTO general VALUES ('{name}', '{variable}', '{value_string}', {value_float})")
    else:
        db(f"UPDATE general SET value_text='{value_string}'" + condition)
        db(f"UPDATE general SET value_float={value_float}" + condition)

def db_read(name, variable):
    condition = f" WHERE name='{name}' and variable = '{variable}'"
    db_str = f"SELECT * FROM general" + condition
    result = db(db_str)
    if len(result) > 0:
        if result[0][2] != "": return result[0][2]
        else: return result[0][3]
    # Manage null responses
    if variable in ["map50", "map95"]: return 0
    # print("DB Read failure", name, variable)

def db_read_time(name, variable):
    # print(variable)
    result = db_read(name, variable)
    if result is None: return timedelta(minutes=0)
    t = datetime.strptime(result, "%H:%M:%S")
    delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    return delta


def db_read_all():
    db_str = f"SELECT * FROM general"
    result = db(db_str)
    for x in result:
        print(x)

# db_read_all()