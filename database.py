import hashlib
import mysql.connector
import pandas as pd
import tkinter.messagebox as tkMessageBox

connection_db = mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",

)


def init_database():
    global connection_db

    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("""CREATE DATABASE IF NOT EXISTS rentacar""")

    mycursor.execute("USE rentacar;")

    mycursor.execute("""CREATE TABLE IF NOT EXISTS flags(
                        name VARCHAR(255) PRIMARY KEY,
                        value INT NOT NULL
                        );""")

    # Creating our database for login information
    mycursor.execute("""CREATE TABLE IF NOT EXISTS masteruser(id INT AUTO_INCREMENT PRIMARY KEY,
    user TEXT NOT NULL,password TEXT NOT NULL)""")

    check_flag_query = "SELECT * FROM flags WHERE name='default_user_created'"
    mycursor.execute(check_flag_query)
    result = mycursor.fetchone()

    if not result:
        def_pass = "admin".encode('utf-8')
        hash_pw = hashlib.sha3_256(def_pass).hexdigest()
        insert_flag_query = "INSERT INTO flags (name, value) VALUES ('default_user_created', 1)"
        mycursor.execute(insert_flag_query)
        sql = "INSERT INTO masteruser (user, password) VALUES (%s, %s)"
        val = ("admin", hash_pw)
        mycursor.execute(sql, val)
        mydb.commit()

    # Creating database for client information
    mycursor.execute("""CREATE TABLE IF NOT EXISTS clients(id INT AUTO_INCREMENT PRIMARY KEY, name TEXT NOT NULL,
    surname TEXT NOT NULL,birthday TEXT NOT NULL, gender TEXT NOT NULL, no_id TEXT NOT NULL,address TEXT NOT NULL, 
    phone TEXT NOT NULL, email TEXT NOT NULL, date_from TEXT NOT NULL, date_until TEXT NOT NULL, 
    car TEXT NOT NULL, plates TEXT NOT NULL)""")

    # Creating database for cars
    mycursor.execute("""CREATE TABLE IF NOT EXISTS cars(id INT AUTO_INCREMENT PRIMARY KEY, mark TEXT NOT NULL, 
    model TEXT NOT NULL, year INT, plates TEXT NOT NULL, reg_date TEXT NOT NULL, available TEXT NOT NULL, 
    other TEXT NOT NULL)""")

    # Creating database for client archive
    mycursor.execute("""CREATE TABLE IF NOT EXISTS archive(id INT AUTO_INCREMENT PRIMARY KEY, name TEXT NOT NULL,
    surname TEXT NOT NULL,birthday TEXT NOT NULL, gender TEXT NOT NULL, no_id TEXT NOT NULL,address TEXT NOT NULL, 
    date_from TEXT NOT NULL, date_until TEXT NOT NULL, car TEXT NOT NULL)""")


def login(uname, pwd):
    global connection_db
    enc_pass = pwd.encode('utf-8')
    mycursor = mydb.cursor(buffered=True)
    # select query
    mycursor.execute("USE rentacar;")
    sql = "SELECT password FROM masteruser WHERE user = %s"
    val = (uname,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    db_hash_pw = result[0]
    db_hash_inpout = hashlib.sha3_256(enc_pass).hexdigest()
    if db_hash_inpout.strip("") == db_hash_pw:
        return True


def search_client(arg):
    global connection_db
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("USE rentacar;")
    query = "SELECT * FROM clients WHERE name LIKE %s"
    mycursor.execute(query, (arg,))
    fetch = mycursor.fetchall()
    for i in fetch:
        return i


def add_client(name, surname, gender, no_id, birthday, address, phone, email, date_from, date_until, car, plates):
    global connection_db
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("USE rentacar;")
    insert_fields = "INSERT INTO clients(name,surname,gender,no_id,birthday,address, phone, email, date_from, " \
                    "date_until, car, plates) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
    mycursor.execute(insert_fields,
                     (name, surname, gender, no_id, birthday, address, phone, email, date_from, date_until, car,plates))
    mydb.commit()


def update_client(name, surname, gender, no_id, birthday, address, phone, email, date_from,
                  date_until, car, plates, selected_item):
    global connection_db
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("USE rentacar;")
    mycursor.execute("UPDATE clients SET name=%s,surname=%s,birthday=%s,gender=%s,no_id=%s,address=%s,phone=%s,email=%s"
                     ",date_from=%s,date_until=%s,car=%s,plates=%s WHERE id=%s", (
                         name, surname, birthday, gender, no_id, address, phone, email, date_from, date_until, car,
                         plates, selected_item[0]))
    mydb.commit()


def delete_client(selected_item):
    global connection_db
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("USE rentacar;")
    mycursor.execute("SELECT * FROM clients WHERE id = %s" % selected_item[0])
    rows = mycursor.fetchall()
    df = pd.DataFrame(rows)
    df.to_csv('archive.csv', sep='\t', index=False, mode='a', header=False)
    mycursor.execute("DELETE FROM clients WHERE id = %s" % selected_item[0])
    mydb.commit()


def show_car():
    global connection_db
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("USE rentacar;")
    # SELECT DISTINCT will display only one value if there duplicate values in our table
    mycursor.execute("SELECT DISTINCT mark, model, available FROM cars WHERE available='Available'")
    results = mycursor.fetchall()
    return results


def fetch_plates(mark, model):
    global connection_db
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("USE rentacar;")
    mycursor.execute("SELECT plates FROM cars WHERE mark = %s AND model = %s AND available=%s", (mark, model, 'Available'))
    result = mycursor.fetchall()
    plates = [row[0] for row in result]
    return plates


def display_data():
    global connection_db
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("USE rentacar;")
    mycursor.execute("SELECT * FROM clients")
    fetch = mycursor.fetchall()
    return fetch


def display_car():
    global connection_db
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("USE rentacar;")
    mycursor.execute("SELECT * FROM cars")
    fetch = mycursor.fetchall()
    return fetch


def save_car(mark, model, year, plates, reg_date, available, other):
    global connection_db
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("USE rentacar;")
    insert_fields = "INSERT INTO cars(mark,model,year,plates,reg_date,available,other) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    mycursor.execute(insert_fields, (mark, model, year, plates, reg_date, available, other))
    mydb.commit()


def update_car(mark, model, year, plates, reg_date, available, other, selected_item):
    global connection_db
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("USE rentacar;")
    mycursor.execute("UPDATE cars SET mark=%s,model=%s,year=%s,plates=%s,reg_date=%s,available=%s,other=%s WHERE id=%s",
                     (mark, model, year, plates, reg_date, available, other, selected_item[0]))
    mydb.commit()


def delete_car(selected_item):
    global connection_db
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("USE rentacar;")
    mycursor.execute("DELETE FROM cars WHERE id = %s" % selected_item[0])
    mydb.commit()


def save_employee(user, password):
    global connection_db
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("USE rentacar;")
    insert_fields = "INSERT INTO masteruser(user,password) VALUES (%s,%s)"
    mycursor.execute(insert_fields, (user, password))
    mydb.commit()


def update_employee(user, password, selected_item):
    global connection_db
    enc_pass = password.encode('utf-8')
    db_hash_pw = hashlib.sha3_256(enc_pass).hexdigest()
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("USE rentacar;")
    mycursor.execute("UPDATE masteruser SET user=%s,password=%s WHERE id=%s",
                     (user, db_hash_pw, selected_item[0]))
    mydb.commit()


def delete_employee(selected_item):
    global connection_db
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("USE rentacar;")
    mycursor.execute("SELECT * FROM masteruser")
    result = mycursor.fetchall()
    count = 0
    for _ in result:
        count += 1
    print(count)
    if count > 1:
        mycursor.execute("DELETE FROM masteruser WHERE id = %s" % selected_item[0])
        tkMessageBox.showinfo("Message", "User deleted successfully")
        mydb.commit()
    else:
        tkMessageBox.showwarning("Warning", "Can't delete the only user left!")


def display_user():
    global connection_db
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("USE rentacar;")
    mycursor.execute("SELECT * FROM masteruser")
    fetch = mycursor.fetchall()
    return fetch
