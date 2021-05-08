import sqlite3
import os.path


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
    conn = sqlite3.connect(db_file)
    return conn

def extract_answer(cursor):
    sql = "SELECT answer FROM matchingType"
    cursor.execute(sql)
    answerList = cursor.fetchall()
    return answerList


#Connected sqlite and python file
#TOMORROW:  Make the actual quiz
#           try ask if pwede nga jumble words na lng instead sa fill in the blanks