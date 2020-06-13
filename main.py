from flask import Flask, render_template, url_for, request, session, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import hashlib 

# Passing the required algorithm as string to the new constructor 
hasher = hashlib.new('ripemd160') 


app = Flask(__name__)

#####################################DATABASE DETAILS#####################################
# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'votesyssecret'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'votesysdb'

# Intialize MySQL
mysql = MySQL(app)


########################################ROUTES##########################################
########Login Page
@app.route('/votesys/login/', methods=['GET', 'POST'])
def login():
   # Output message if something goes wrong...
   msg = ''
   # Check if "email" and "password" POST requests exist (user submitted form)
   if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
      email = request.form['email']
      password = request.form['password']
     
      # Check if account exists using MySQL
      cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute('SELECT * FROM usertab WHERE email = %s AND pass = MD5(%s)', (email,password,))
      # Fetch one record and return result
      account = cursor.fetchone()
      # If account exists in usertab and the supplied password is correct
      if account['category'] == 'voter':# if user is a voter
         # Create session data, we can access this data in other routes
         session['loggedin'] = True
         session['id'] = account['userid']
         session['name'] = account['firstname']
         return redirect(url_for('booth'))
      elif account['category'] == 'admin':# if user is a admin
         # Create session data, we can access this data in other routes
         session['loggedin'] = True
         session['id'] = account['userid']
         session['name'] = account['firstname']
         return redirect(url_for('admin'))
         #msg = hashed
      else:
         # Account doesn't exist or username/password incorrect
         msg = 'Incorrect username/password!'
   #By default (without credentials supply)      
   return render_template('login.html', msg=msg)


########Admin Login Page
@app.route('/votesys/logexed/', methods=['GET', 'POST'])
def logexed():
   # Output message if something goes wrong...
   msg = ''
   # Check if "email" and "password" POST requests exist (user submitted form)
   if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
      email = request.form['email']
      password = request.form['password']
      # Check if account exists using MySQL
      cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute('SELECT * FROM usertab WHERE email = %s AND pass = MD5(%s)', (email,password,))
      # Fetch one record and return result
      account = cursor.fetchone()
      # If account exists in usertab and the supplied password is correct
      if account['category'] == 'admin':
         # Create session data, we can access this data in other routes
         session['loggedin'] = True
         session['id'] = account['userid']
         session['name'] = account['firstname']
         return redirect(url_for('admin'))
      elif account['category'] == 'admin':
         # Create session data, we can access this data in other routes
         session['loggedin'] = True
         session['id'] = account['userid']
         session['name'] = account['firstname']
         return redirect(url_for('admin'))
         #msg = hashed
      else:
         # Account doesn't exist or username/password incorrect
         msg = 'Incorrect username/password!'
         
   return render_template('login.html', msg=msg)


########Logout Page
@app.route('/votesys/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('name', None)
   # Redirect to login page
   return redirect(url_for('login'))

########Registration Page
@app.route('/votesys/register', methods=['GET', 'POST'])
def register():
   # Output message if something goes wrong...
   msg = ''
   # Check if "username", "password" and "email" POST requests exist (user submitted form)
   if request.method == 'POST' and 'surname' in request.form and 'firstname' in request.form and 'midname' in request.form and 'email' in request.form and 'password' in request.form and 'phone' in request.form:
      # Create variables for easy access
      surname = request.form['surname']
      firstname = request.form['firstname']
      midname = request.form['midname']
      phone = request.form['phone']
      email = request.form['email']
      password = request.form['password']
      #hasher.update(password.encode('utf-8'))
      #hashed = hasher.hexdigest()
      category = 'voter'
      
      # Check if account exists using MySQL
      cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute('SELECT * FROM usertab WHERE email = %s', (email,))
      account = cursor.fetchone()
      # If account exists show error and validation checks
      if account:
         msg = 'Account already exists!'
      elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
         msg = 'Invalid email address!'
      elif not surname or not firstname or not midname or not phone or not password or not email:
         msg = 'Please fill out the form!'
      else:
         # Account doesnt exists and the form data is valid, now insert new account into accounts table
         cursor.execute('INSERT INTO usertab (userid, surname, midname, firstname, regdate, phone, email, pass, category) VALUES (NULL, %s, %s, %s, now(), %s, %s, MD5(%s), %s)', (surname, midname, firstname, phone, email, password, category,))
         mysql.connection.commit()
         msg = 'You have successfully registered!'
   elif request.method == 'POST':
      # Form is empty... (no POST data)
      msg = 'Please fill out the form!'
   # Show registration form with message (if any)
   return render_template('register.html', msg=msg)


########Registration Page for admin
@app.route('/votesys/regexed', methods=['GET', 'POST'])
def regexed():
   # Output message if something goes wrong...
   msg = ''
   # Check if "username", "password" and "email" POST requests exist (user submitted form)
   if request.method == 'POST' and 'surname' in request.form and 'firstname' in request.form and 'midname' in request.form and 'email' in request.form and 'password' in request.form and 'phone' in request.form:
      # Create variables for easy access
      surname = request.form['surname']
      firstname = request.form['firstname']
      midname = request.form['midname']
      phone = request.form['phone']
      email = request.form['email']
      password = request.form['password']
      category = 'admin'
      
      # Check if account exists using MySQL
      cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute('SELECT * FROM usertab WHERE email = %s', (email,))
      account = cursor.fetchone()
      # If account exists show error and validation checks
      if account:
         msg = 'Account already exists!'
      elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
         msg = 'Invalid email address!'
      elif not surname or not firstname or not midname or not phone or not password or not email:
         msg = 'Please fill out the form!'
      else:
         # Account doesnt exists and the form data is valid, now insert new account into accounts table
         cursor.execute('INSERT INTO usertab (userid, surname, midname, firstname, regdate, phone, email, pass, category) VALUES (NULL, %s, %s, %s, now(), %s, %s, MD5(%s), %s)', (surname, midname, firstname, phone, email, password, category,))
         mysql.connection.commit()
         msg = 'You have successfully registered!'
   elif request.method == 'POST':
      # Form is empty... (no POST data)
      msg = 'Please fill out the form!'
   # Show registration form with message (if any)
   return render_template('regexed.html', msg=msg)


@app.route('/votesys/booth')
def booth():
   position=[]
   full_name=[]
   # Check if user is loggedin
   if 'loggedin' in session:
      # User is loggedin show them to the booth
      # Fetch Contestants from DB
      cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute('SELECT usertab.userid, usertab.surname, usertab.midname, usertab.firstname, contesttab.position\
                        FROM usertab INNER JOIN contesttab ON usertab.userid=contesttab.userid;')
      contenstants_details = cursor.fetchall()
      cont_userid = [contenstants_details[i][0] for i in range(len(contenstants_details))]
      full_name = [contenstants_details[i][1]+" "+ contenstants_details[i][2]+" "+contenstants_details[i][3] for i in range(len(contenstants_details))]
      position = [contenstants_details[i][4] for i in range(len(contenstants_details))] #returns individual positions
      #Search for voter on voters' table and return value to status
      status =''
      #return render_template('booth.html', userid= session['id'], username=session['name'],cont_userid, full_name, position)
      return render_template('booth.html', userid= session['id'], username=session['name'])
   # User is not loggedin redirect to login page
   return redirect(url_for('login'))


@app.route('/votesys/admin')
def admin():
   # Check if user is loggedin
   if 'loggedin' in session:
      # User is loggedin show them to the booth
      # Check if account exists using MySQL
      cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute('SELECT * FROM contest_2020_tab')
      contenstants = cursor.fetchall()
      return render_template('admin.html', username=session['name'])
   # User is not loggedin redirect to login page
   return redirect(url_for('login'))



@app.route('/votesys/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usertab WHERE userid = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))



@app.route('/votesys/')
def home():
    return 'Hello INdex'
   #return render_template("index.html")



if __name__ == '__main__':
   app.run(debug = True)
   
   