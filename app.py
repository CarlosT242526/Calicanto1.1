from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB = "basedatos.db"

def conectar():
    return sqlite3.connect(DB)

# ================================
# RUTA DE PRUEBA
# ================================
@app.route('/')
def inicio():
    return "Servidor activo"

# ================================
# 👤 REGISTRO DE SOCIOS
# ================================
@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    con = conectar()
    cursor = con.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS socios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            cedula TEXT UNIQUE,
            password TEXT
        )
    """)

    try:
        cursor.execute(
            "INSERT INTO socios (nombre, cedula, password) VALUES (?, ?, ?)",
            (data['nombre'], data['cedula'], data['password'])
        )
        con.commit()
        mensaje = "Usuario registrado correctamente"
        status = 200
    except sqlite3.IntegrityError:
        mensaje = "❌ Ya existe un usuario con esa cédula"
        status = 400

    con.close()
    return jsonify({"mensaje": mensaje}), status

# ================================
# 🔐 LOGIN
# ================================
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    con = conectar()
    cursor = con.cursor()

    cursor.execute(
        "SELECT * FROM socios WHERE cedula=? AND password=?",
        (data['cedula'], data['password'])
    )
    usuario = cursor.fetchone()
    con.close()

    if usuario:
        return jsonify({"mensaje": f"✅ Bienvenido {usuario[1]}"})
    else:
        return jsonify({"mensaje": "❌ La cédula o la contraseña no coinciden. Si no tienes cuenta, por favor regístrate."}), 401

# ================================
# ♻️ REGISTRO DE RESIDUOS
# ================================
@app.route('/residuos', methods=['POST'])
def residuos():
    data = request.get_json()
    con = conectar()
    cursor = con.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS residuos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            peso REAL,
            fecha TEXT,
            origen TEXT,
            observaciones TEXT
        )
    """)

    cursor.execute("""
        INSERT INTO residuos (tipo, peso, fecha, origen, observaciones)
        VALUES (?, ?, ?, ?, ?)
    """, (data['tipo'], data['peso'], data['fecha'], data['origen'], data['obs']))

    con.commit()
    con.close()
    return jsonify({"mensaje": "Residuo guardado correctamente"})

# ================================
# 🤝 REGISTRO DE ACTIVIDADES
# ================================
@app.route('/actividad', methods=['POST'])
def actividad():
    data = request.get_json()
    con = conectar()
    cursor = con.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS actividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            descripcion TEXT,
            cantidad REAL,
            fecha TEXT,
            horas REAL
        )
    """)

    cantidad = float(data['cantidadTratada']) if data['cantidadTratada'] not in ["", "N/A"] else 0

    cursor.execute("""
        INSERT INTO actividades (tipo, descripcion, cantidad, fecha, horas)
        VALUES (?, ?, ?, ?, ?)
    """, (data['tipo'], data['descripcion'], cantidad, data['fecha'], float(data['horas'])))

    con.commit()
    con.close()
    return jsonify({"mensaje": "Actividad guardada correctamente"})

# ================================
# EJECUTAR SERVIDOR
# ================================
if __name__ == '__main__':
    app.run(debug=True)
