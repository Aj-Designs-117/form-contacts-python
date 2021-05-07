from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# inicializacion de flash
app = Flask(__name__)

# Conexcion a MySQL
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'contacts'
mysql = MySQL(app)

#Inicializando una sesion
app.secret_key = "mysecretkey"

@app.route('/')
def index():

    query = mysql.connection.cursor()
    query.execute("SELECT * FROM contacts")
    data = query.fetchall()

    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():

    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        query = mysql.connection.cursor()
        query.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)', (fullname, phone, email) )
        mysql.connection.commit()
    
    flash("Contacto agregado correctmente")
    return redirect(url_for('index'))        

@app.route('/edit/<id>')
def get_contact(id):
    query = mysql.connection.cursor()
    query.execute("SELECT * FROM contacts WHERE id = %s", (id))
    data = query.fetchall()

    return render_template('edit.html', contact = data[0])


@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        query = mysql.connection.cursor()
        query.execute(""" 
            UPDATE contacts 
            SET fullname = %s, 
                phone = %s, 
                email = %s
            WHERE id = %s
        """, (fullname, phone, email, id))
        mysql.connection.commit()

    flash("Se ha actualizado correctamente")
    return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    query = mysql.connection.cursor()
    query.execute("DELETE FROM contacts WHERE id = {0}".format(id))
    mysql.connection.commit()

    flash("Contacto eliminado correctmente")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)