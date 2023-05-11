from flask import Flask, render_template, url_for, Response, jsonify, request
import sqlite3
from sqlalchemy import create_engine, text
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route("/")
def index():
    #------------------- sqlite3 -------------------
    # connection = sqlite3.connect("function_script/interface_hw.db")
    # # Set the row_factory attribute
    # connection.row_factory = sqlite3.Row
    # #create a cursor object to execute sql command
    # cursor = connection.cursor()
    # # Query the data from the table
    # cursor.execute("SELECT * FROM list_interface")

    # rows = cursor.fetchall()

    # interfaces_list = list()
    # for row in rows:
    #     interfaces_list.append(dict(row))
    # connection.close()

    #-----------------SQLAlchemy --------------------
    
    database_path = "sqlite:///function_script/interface_hw.db"
    engine = create_engine(database_path)
    connection = engine.connect()
    sql_query = text("SELECT * FROM list_interface")
    result = connection.execute(sql_query).fetchall()

    interfaces_list = [row._mapping for row in result]

    return render_template("index.html", interfaces_list=interfaces_list)

@app.route("/api", methods=["GET"])
def interfaces():
    #------------------- sqlite3 -------------------
    connection = sqlite3.connect("function_script/interface_hw.db")
    # Set the row_factory attribute
    connection.row_factory = sqlite3.Row
    #create a cursor object to execute sql command
    cursor = connection.cursor()
    # Query the data from the table
    cursor.execute("SELECT * FROM list_interface")

    rows = cursor.fetchall()

    interfaces_list = list()
    for row in rows:
        interfaces_list.append(dict(row))
    connection.close()

    return interfaces_list

@app.route("/search", methods=["GET","POST"])
def search():

    query = request.args.get("msan_name")
    if query:
        #------------------- sqlite3 -------------------
        connection = sqlite3.connect("function_script/interface_hw.db")
        # Set the row_factory attribute
        connection.row_factory = sqlite3.Row
        #create a cursor object to execute sql command
        cursor = connection.cursor()
        # Query the data from the table
        query_sql = f"SELECT * FROM list_interface WHERE Description like '%{query}%'"
        cursor.execute(query_sql)

        rows = cursor.fetchall()

        interfaces_list = list()
        for row in rows:
            interfaces_list.append(dict(row))
        connection.close()
    else:
        connection = sqlite3.connect("function_script/interface_hw.db")
        # Set the row_factory attribute
        connection.row_factory = sqlite3.Row
        #create a cursor object to execute sql command
        cursor = connection.cursor()
        # Query the data from the table
        query_sql = f"SELECT * FROM list_interface"
        cursor.execute(query_sql)

        rows = cursor.fetchall()

        interfaces_list = list()
        for row in rows:
            interfaces_list.append(dict(row))
        connection.close()
    return interfaces_list