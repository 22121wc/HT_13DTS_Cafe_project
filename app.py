from flask import Flask, render_template, request, redirect
import sqlite3
from sqlite3 import Error
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt  =Bcrypt(app)
app.secret_key="Abra"
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

@app.route('/signup', methods=['POST','GET'])
def render_signup_page():
    if request.method == "POST":
        fname = request.form.get('user_fname').title().strip()
        lname = request.form.get('user_lname').title().strip()
        email = request.form.get('user_email').lower().strip()
        password = request.form.get('user_password')
        password2 = request.form.get('user_password2')

        if password != password2:
            return redirect("\signup?error=passwords+do+not+match")
        if len(password) < 8:
            return redirect("\signup?error=password+must+be+over+eight+characters")

        hashed_password = bcrypt.generate_password_hash(password)

        con = connect_database(DATABASE)
        query_insert = "INSERT INTO user (first_name, last_name, email, password) VALUES (?,?,?,?)"

        cur = con.cursor()
        cur.execute(query_insert, (fname, lname, email, hashed_password))
        con.commit()
        con.close
    return render_template('signup.html')

@app.route('/login', methods=['POST','GET'])
def render_login_page():
    return render_template('login.html')

@app.route('/menu/<cat_id>')
def render_menu_page(cat_id):
    con = connect_database(DATABASE)
    query = "SELECT name, description, volume, image, price FROM products WHERE fk_cat_id = ?"
    query_cat_list = "SELECT * FROM categories"
    cur = con.cursor()
    cur.execute(query, (cat_id,))
    product_list = cur.fetchall()
    cur.execute(query_cat_list)
    cat_list = cur.fetchall()
    print(product_list)
    print(cat_list)
    con.close()
    return render_template('menu.html', product_list = product_list, cat_list = cat_list)


@app.route('/contact')
def render_contact_page():
    return render_template('contact.html')


app.run(host='0.0.0.0', debug=True)
