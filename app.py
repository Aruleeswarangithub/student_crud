from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# DB init
def init_db():
    conn = sqlite3.connect('StudentDB.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        roll_number TEXT NOT NULL,
                        email TEXT NOT NULL,
                        mobile TEXT NOT NULL
                    )''')
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('StudentDB.db')
    cursor = conn.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()
    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    roll_number = request.form['roll_number']
    email = request.form['email']
    mobile = request.form['mobile']
    conn = sqlite3.connect('StudentDB.db')
    conn.execute("INSERT INTO students (name, roll_number, email, mobile) VALUES (?, ?, ?, ?)",
                 (name, roll_number, email, mobile))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>')
def edit(id):
    conn = sqlite3.connect('StudentDB.db')
    cursor = conn.execute("SELECT * FROM students WHERE id = ?", (id,))
    student = cursor.fetchone()
    conn.close()
    return render_template('edit.html', student=student)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    name = request.form['name']
    roll_number = request.form['roll_number']
    email = request.form['email']
    mobile = request.form['mobile']
    conn = sqlite3.connect('StudentDB.db')
    conn.execute("UPDATE students SET name = ?, roll_number = ?, email = ?, mobile = ? WHERE id = ?",
                 (name, roll_number, email, mobile, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('StudentDB.db')
    conn.execute("DELETE FROM students WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
