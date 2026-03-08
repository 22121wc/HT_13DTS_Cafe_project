from flask import Flask, render_template, request, redirect, session
import sqlite3
from sqlite3 import Error
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key= "Abra"
DATABASE = "cafe.db"

def is_logged_in():
    if (session.get("user_id") is None):
        return False
    else:
        return True
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
    return render_template('home.html', logged_in = is_logged_in())

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
        con.close()
        return redirect("/login")
    return render_template('signup.html', logged_in = is_logged_in())

@app.route('/admin', methods=['POST','GET'])
def render_admin_page():
    if not is_logged_in():
        return redirect('/message=not+logged+in')
    con=connect_database(DATABASE)
    query = "SELECT * FROM categories"
    cur = con.cursor()
    cur.execute(query)
    results= cur.fetchall()
    print(f'results fromc ategory table = {results}')
    con.close()
    return render_template('admin.html', logged_in=is_logged_in(), category_list=results)
@app.route('/login', methods=['POST','GET'])
def render_login_page():
    #collect info from db
    # check against form
    # save info of the session
    if is_logged_in():
        return redirect('/menu/1')
    if request.method == "POST":
        email = request.form['user_email'].strip().lower()
        password = request.form['user_password']
        query = "SELECT user_id, first_name, password FROM user WHERE email = ?"
        con = connect_database(DATABASE)
        cur = con.cursor()
        cur.execute(query, (email,))
        user_info = cur.fetchone()
        print(user_info)
        cur.close()
        try:
            user_id = user_info[0]
            first_name = user_info[1]
            user_password = user_info[2]
        except TypeError:
            return redirect("/login?error=email+or+password+invalid")

        if not bcrypt.check_password_hash(user_password, password):
            return redirect("/login?error=email+or+password+invalid")
        session["email"] = email
        session["user_id"] = user_id
        session["first_name"] = first_name
        print(session)
        return redirect("/")
    return render_template('login.html', logged_in = is_logged_in())
@app.route('/logout', methods=['POST','GET'])
def render_logout():
    print(session)
    session.clear()
    print(session)
    return redirect('/login')

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
    return render_template('menu.html', product_list = product_list, cat_list = cat_list, logged_in = is_logged_in())


@app.route('delete_category', methods['POST','GET'])
def delete_category():
    if not is_logged_in()
        return redirect('/message=not+logged+in')

    if request.method == 'POST':
        category = request.form.get('select_cat')
        print(category)
        category = category.strip("(")
        category = category.strip(")")
        category = category.split(", ")

        cat_id = category[0]
        cat_name = category[1]
        print(f'cat_id = {cat_id} and cat name = {cat_name}')
        return render_template('delete_confirm.html', cat_id=cat_id, cat_name=cat_name, type=category...)

app.run(host='0.0.0.0', debug=True)
