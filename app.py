from flask import Flask, render_template
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

DATABASE = "cafe.db"

def connect_database(db_file):
    """
    Creates a connection with the database
    :param db_file:
    :return:
    """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
        print("An error occured when connecting to the database")
        return None
@app.route('/')
def render_homepage():
    return render_template('home.html')


@app.route('/menu')
def render_menu_page():
    con = connect_database(DATABASE)
    query = "SELECT name, description, volume, image, price FROM products"
    cur = con.cursor()
    cur.execute(query)
    product_list = cur.fetchall()
    con.close()
    return render_template('menu.html')


@app.route('/contact')
def render_contact_page():
    return render_template('contact.html')


app.run(host='0.0.0.0', debug=True)
