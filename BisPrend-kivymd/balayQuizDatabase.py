import sqlite3
import os.path
from os import listdir, getcwd
from IPython.core.display import Image

#List Files
def get_picture_list(rel_path):
    abs_path = os.path.join(os.getcwd(), rel_path)
    print('abs_path = ' + abs_path)
    dir_files = os.listdir(abs_path)
    return dir_files


picture_list = get_picture_list('balay')
print(picture_list)

#Create database
def create_or_open_db(db_file):
    db_is_new = not os.path.exists(db_file)
    conn = sqlite3.connect(db_file)
    if db_is_new:
        print("Creating schema")
        sql = '''create table if not exists fillintheblanks(
        category VARCHAR,
        image BLOB,
        type TEXT,
        file_name TEXT,
        question VARCHAR,
        answer VARCHAR);'''
        conn.execute(sql)
    else:
        print("Schema exists")
    return conn

def insert_picture(conn, picture_file, category, question, answer):
    print("Insert_picture")
    with open(picture_file, 'rb') as input_file:
        ablob = input_file.read()
        base=os.path.basename(picture_file)
        afile, ext = os.path.splitext(base)
        data = (category, sqlite3.Binary(ablob), ext, afile, question, answer)
        sql = '''INSERT INTO fillintheblanks
        (category, image, type, file_name, question, answer) VALUES (?,?,?,?,?,?);'''
        conn.execute(sql, data)
        conn.commit()
    print("finish insert")

conn = create_or_open_db('BalayQuiz.db')

#Creating schema
picture_file = "./balay/ate.png"
insert_picture(conn, picture_file, "Pamilya", "ate", "ate")
conn.close()

def extract_picture(cursor, image_name):
    sql = "SELECT image,type,file_name FROM fillintheblanks WHERE answer = :ans"
    param = {'ans': image_name}
    cursor.execute(sql, param)
    ablob, ext, afile = cursor.fetchone()
    filename = afile + ext
    with open(filename, 'wb') as output_file:
        output_file.write(ablob)
    print("Success")
    return filename

conn = create_or_open_db('BalayQuiz.db')
cur = conn.cursor()
filename = extract_picture(cur,"ate")
cur.close()
conn.close()

#Connected sqlite and python file
#TOMORROW:  Make the actual quiz
#           try ask if pwede nga jumble words na lng instead sa fill in the blanks