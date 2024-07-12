from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn=sqlite3.connect('database.db')
    return conn

def init_db():
    conn=get_db_connection()
    with app.open_resource('schema.sql', mode='r') as f:
        conn.cursor().executescript(f.read())
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        date_of_birth = request.form['date_of_birth']

        conn = get_db_connection()
        c = conn.cursor()
        c.execute('Insert into entries (name, email, age, date_of_birth) values (?, ?, ?, ?)', (name, email, int(age), date_of_birth))
        conn.commit()
        conn.close()
        return redirect(url_for('entries'))

    return render_template('index.html')
@app.route('/entries')
def entries():
    conn = get_db_connection()
    c=conn.cursor()
    cursor = c.execute('Select * from entries')
    entries = cursor.fetchall()
    conn.close()
    return render_template('entries.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True)