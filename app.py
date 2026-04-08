from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()

    con = sqlite3.connect("basedatos.db")
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
        (data['nombre'], data['cedula'], data['password'])
    )

    con.commit()
    con.close()

    return jsonify({"mensaje": "Guardado correctamente"})

app.run(debug=True)