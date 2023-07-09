import pyotp    #generates one-time passwords
import sqlite3  #database for username/passwords
import hashlib  #secure hashes and message digests
import uuid     #for creating universally unique identifiers
from flask import Flask, request
from datetime import datetime

app = Flask(__name__) 

db_name = 'test.db' 

@app.route('/')
def index():
    return '¡Bienvenido al examen de evolución de sistemas de contraseñas!'

######################################### Hash Password #########################################################
@app.route('/signup/v1', methods=['POST'])
def signup_v1():
    conn = sqlite3.connect(db_name)

    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USER_HASH
           (USERNAME  TEXT    PRIMARY KEY NOT NULL,
            PASSWORD  TEXT    NOT NULL);''')  # Creación de tabla si no existe
    conn.commit()

    username = request.form['username']
    password = request.form['password']
    hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Hash de la contraseña

    try:
        c.execute("INSERT INTO USER_HASH (USERNAME,PASSWORD) "
                  "VALUES (?, ?)", (username, hashed_password))  # Inserción de los datos del usuario
        conn.commit()
    except sqlite3.IntegrityError:
        return "El nombre de usuario ya ha sido registrado."

    conn.close()
    return "Registro exitoso"

def verify_hash(username, password):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    c.execute("SELECT PASSWORD FROM USER_HASH WHERE USERNAME = ?", (username,))
    records = c.fetchone()

    if records is None:
        return False

    hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Hash de la contraseña para compararla
    return records[0] == hashed_password

@app.route('/login/v1', methods=['POST'])
def login_v1():
    if request.method == 'POST':
        success = verify_hash(request.form['username'], request.form['password'])
        # Log the login attempt
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS LOGIN_ATTEMPTS
               (ID        INTEGER PRIMARY KEY AUTOINCREMENT,
                USERNAME  TEXT    NOT NULL,
                TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP,
                SUCCESS   INT     NOT NULL);''')
        conn.commit()
        c.execute("INSERT INTO LOGIN_ATTEMPTS (USERNAME,SUCCESS) "
                  "VALUES (?, ?)", (request.form['username'], int(success)))
        conn.commit()
        conn.close()
        if success:
            return 'Inicio de sesión exitoso'
        else:
            return 'Nombre de usuario/contraseña inválidos'
    else:
        return 'Invalid Method'

@app.route('/login_attempts', methods=['GET'])
def login_attempts():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM LOGIN_ATTEMPTS")
    records = c.fetchall()
    conn.close()
    return '\n'.join(f'{record[1]} attempted to log in at {record[2]}. Success: {bool(record[3])}' for record in records)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4850)  # Running the app on port 4850
