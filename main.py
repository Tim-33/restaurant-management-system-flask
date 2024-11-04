from flask import Flask,render_template, request
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
 
app = Flask(__name__)

load_dotenv()

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT'))
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config["MYSQL_CUSTOM_OPTIONS"] = {"ssl": {"ca": os.getenv('MYSQL_SSL_CA')}}
 
mysql = MySQL(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test")
def test():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM test")
    result = cursor.fetchall()
    return str(result)