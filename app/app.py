from flask import Flask, render_template_string
import os
import pymysql
from pymysql.cursors import DictCursor, Cursor  
app = Flask(__name__)
spartak="champion"
DB_HOST = os.getenv('DB_HOST', 'db')
DB_PORT = int(os.getenv('DB_PORT', 3306))  
DB_NAME = os.getenv('DB_NAME', 'mydb')
DB_USER = os.getenv('DB_USER', 'myuser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'mypassword')

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        cursorclass=DictCursor  
    )

def init_db():
    conn = get_db_connection()
    cur = conn.cursor(Cursor)  
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbEY,
            name VARCHAR(100),
            email VARCHAR(100)
        )
    ''')
    cur.execute('SELECT COUNT(*) FROM users')
    if cur.fetchone()[0] == 0:  
        cur.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com'), ('Bob', 'bob@example.com'), ('Charlie', 'charlie@example.com')")
        conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()  
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()  
    cur.close()
    conn.close()
    html = '''
    <h1>Данные из БД (MySQL)</h1>
    <table border="1">
        <tr><th>ID</th><th>Name</th><th>Email</th></tr>
        {% for user in users %}
        <tr><td>{{ user['id'] }}</td><td>{{ user['name'] }}</td><td>{{ user['email'] }}</td></tr>
        {% endfor %}
    </table>
    <p>Данные идентичны хранящимся в БД.</p>
    '''
    return render_template_string(html, users=users)

if __name__ == '__main__':
    init_db()  
    app.run(host='0.0.0.0', port=5000, debug=True)
