from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# 🔹 Conexión a la base de datos
def conectar():
    return sqlite3.connect("basedatos.db")

# 🔹 RUTA PRINCIPAL (para probar servidor)
@app.route('/')
def inicio():
    return "Servidor activo"

# ================================
# 👤 REGISTRO DE USUARIOS
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
        cedula TEXT,
        password TEXT
    )
    """)

    cursor.execute(
        "INSERT INTO socios (nombre, cedula, password) VALUES (?, ?, ?)",
        (
            data['nombre'].strip(),
            data['cedula'].strip(),
            data['password'].strip()
        )
    )

    con.commit()
    con.close()

    return jsonify({"mensaje": "Usuario registrado correctamente"})

# ================================
# 🔐 LOGIN
# ================================
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    cedula = data['cedula'].strip()
    password = data['password'].strip()

    con = conectar()
    cursor = con.cursor()

    # 🔍 Buscar usuario SOLO por cédula
    cursor.execute("SELECT * FROM socios WHERE cedula=?", (cedula,))
    usuario = cursor.fetchone()

    con.close()

    # ❌ Si no existe
    if not usuario:
        return jsonify({"mensaje": "Usuario no existe"})

    # ❌ Si la contraseña no coincide
    if usuario[3] != password:
        return jsonify({"mensaje": "Contraseña incorrecta"})

    # ✅ Todo correcto
    return jsonify({"mensaje": "Login correcto"})
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
    """, (
        data['tipo'],
        data['peso'],
        data['fecha'],
        data['origen'],
        data['obs']
    ))

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
        cantidad TEXT,
        fecha TEXT,
        horas TEXT
    )
    """)

    cursor.execute("""
        INSERT INTO actividades (tipo, descripcion, cantidad, fecha, horas)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data['tipo'],
        data['descripcion'],
        data['cantidadTratada'],
        data['fecha'],
        data['horas']
    ))

    con.commit()
    con.close()

    return jsonify({"mensaje": "Actividad guardada correctamente"})

# ================================
# 🚀 EJECUTAR SERVIDOR
# ================================
if __name__ == '__main__':
    app.run(debug=True)
