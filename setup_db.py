"""
setup_db.py
Crea la base de datos SQLite y la carga con datos de ejemplo.
Ejecutar una sola vez antes de correr analisis.py
"""

import sqlite3
import random
from datetime import date, timedelta

# ── Configuración ──────────────────────────────────────────────
DB_PATH = "kiosco.db"
FECHA_INICIO = date(2024, 1, 1)
FECHA_FIN    = date(2024, 12, 31)
SEMILLA      = 42          # para resultados reproducibles

random.seed(SEMILLA)

# ── Datos maestros ─────────────────────────────────────────────
PRODUCTOS = [
    # (nombre, categoria, precio_unitario)
    ("Coca-Cola 500ml",   "Bebidas",    350),
    ("Agua mineral",      "Bebidas",    200),
    ("Jugo Cepita",       "Bebidas",    280),
    ("Alfajor Milka",     "Golosinas",  450),
    ("Chiclets",          "Golosinas",   80),
    ("Papas fritas",      "Snacks",     320),
    ("Maní con chocolate","Snacks",     180),
    ("Cigarrillos",       "Tabaco",    1200),
    ("Encendedor",        "Varios",     350),
    ("Diario Clarín",     "Prensa",     400),
]

def crear_tablas(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS productos (
            id_producto   INTEGER PRIMARY KEY,
            nombre        TEXT    NOT NULL,
            categoria     TEXT    NOT NULL,
            precio_unit   REAL    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS ventas (
            id_venta    INTEGER PRIMARY KEY AUTOINCREMENT,
            id_producto INTEGER NOT NULL,
            fecha       TEXT    NOT NULL,
            cantidad    INTEGER NOT NULL,
            total       REAL    NOT NULL,
            FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
        );
    """)

def cargar_productos(conn):
    conn.executemany(
        "INSERT INTO productos (nombre, categoria, precio_unit) VALUES (?, ?, ?)",
        PRODUCTOS
    )

def generar_ventas(conn):
    """Genera ~1500 registros de venta distribuidos a lo largo del año."""
    ventas = []
    fecha_actual = FECHA_INICIO

    while fecha_actual <= FECHA_FIN:
        # Entre 2 y 6 ventas por día
        for _ in range(random.randint(2, 6)):
            id_producto = random.randint(1, len(PRODUCTOS))
            precio      = PRODUCTOS[id_producto - 1][2]
            cantidad    = random.randint(1, 5)
            total       = precio * cantidad
            ventas.append((id_producto, fecha_actual.isoformat(), cantidad, total))

        fecha_actual += timedelta(days=1)

    conn.executemany(
        "INSERT INTO ventas (id_producto, fecha, cantidad, total) VALUES (?, ?, ?, ?)",
        ventas
    )
    return len(ventas)


def main():
    print("Creando base de datos...")
    conn = sqlite3.connect(DB_PATH)

    crear_tablas(conn)
    cargar_productos(conn)
    n = generar_ventas(conn)

    conn.commit()
    conn.close()

    print(f"Base de datos '{DB_PATH}' creada exitosamente.")
    print(f"  - {len(PRODUCTOS)} productos cargados")
    print(f"  - {n} registros de ventas generados")
    print("\nAhora podés ejecutar: python analisis.py")


if __name__ == "__main__":
    main()
