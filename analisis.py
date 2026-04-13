"""
analisis.py
Análisis de ventas del kiosco usando SQL + pandas.
Requiere haber ejecutado setup_db.py primero.
"""

import sqlite3
import pandas as pd

DB_PATH = "kiosco.db"

# ── Conexión ───────────────────────────────────────────────────
conn = sqlite3.connect(DB_PATH)

print("=" * 55)
print("   ANÁLISIS DE VENTAS — KIOSCO 2024")
print("=" * 55)


# ── 1. Resumen general ─────────────────────────────────────────
query_resumen = """
    SELECT
        COUNT(*)                        AS total_transacciones,
        SUM(total)                      AS facturacion_total,
        ROUND(AVG(total), 2)            AS ticket_promedio,
        SUM(cantidad)                   AS unidades_vendidas
    FROM ventas;
"""
resumen = pd.read_sql_query(query_resumen, conn).iloc[0]

print("\n📊 RESUMEN GENERAL")
print(f"  Transacciones:      {int(resumen['total_transacciones']):,}")
print(f"  Facturación total:  ${resumen['facturacion_total']:,.0f}")
print(f"  Ticket promedio:    ${resumen['ticket_promedio']:,.2f}")
print(f"  Unidades vendidas:  {int(resumen['unidades_vendidas']):,}")


# ── 2. Top 5 productos por facturación ────────────────────────
query_top = """
    SELECT
        p.nombre,
        p.categoria,
        SUM(v.total)    AS facturacion,
        SUM(v.cantidad) AS unidades
    FROM ventas v
    JOIN productos p ON v.id_producto = p.id_producto
    GROUP BY p.id_producto
    ORDER BY facturacion DESC
    LIMIT 5;
"""
top_productos = pd.read_sql_query(query_top, conn)

print("\n🏆 TOP 5 PRODUCTOS POR FACTURACIÓN")
print(f"  {'Producto':<25} {'Facturación':>12} {'Unidades':>10}")
print("  " + "-" * 50)
for _, row in top_productos.iterrows():
    print(f"  {row['nombre']:<25} ${row['facturacion']:>10,.0f} {int(row['unidades']):>10,}")


# ── 3. Facturación por categoría ──────────────────────────────
query_cat = """
    SELECT
        p.categoria,
        SUM(v.total)                              AS facturacion,
        ROUND(SUM(v.total) * 100.0 /
              (SELECT SUM(total) FROM ventas), 1) AS porcentaje
    FROM ventas v
    JOIN productos p ON v.id_producto = p.id_producto
    GROUP BY p.categoria
    ORDER BY facturacion DESC;
"""
categorias = pd.read_sql_query(query_cat, conn)

print("\n📂 FACTURACIÓN POR CATEGORÍA")
print(f"  {'Categoría':<15} {'Facturación':>12} {'%':>8}")
print("  " + "-" * 38)
for _, row in categorias.iterrows():
    barra = "█" * int(row['porcentaje'] / 3)
    print(f"  {row['categoria']:<15} ${row['facturacion']:>10,.0f} {row['porcentaje']:>6.1f}%  {barra}")


# ── 4. Ventas por mes ─────────────────────────────────────────
query_mes = """
    SELECT
        strftime('%m', fecha)   AS mes,
        SUM(total)              AS facturacion,
        COUNT(*)                AS transacciones
    FROM ventas
    GROUP BY mes
    ORDER BY mes;
"""
meses_df = pd.read_sql_query(query_mes, conn)

MESES = ["Ene","Feb","Mar","Abr","May","Jun",
         "Jul","Ago","Sep","Oct","Nov","Dic"]

print("\n📅 FACTURACIÓN MENSUAL")
print(f"  {'Mes':<6} {'Facturación':>12} {'Transacciones':>15}")
print("  " + "-" * 36)
for _, row in meses_df.iterrows():
    nombre_mes = MESES[int(row['mes']) - 1]
    print(f"  {nombre_mes:<6} ${row['facturacion']:>10,.0f} {int(row['transacciones']):>15,}")

# Mes con mayor y menor facturación
idx_max = meses_df['facturacion'].idxmax()
idx_min = meses_df['facturacion'].idxmin()
mes_max = MESES[int(meses_df.loc[idx_max, 'mes']) - 1]
mes_min = MESES[int(meses_df.loc[idx_min, 'mes']) - 1]
print(f"\n  ↑ Mejor mes:  {mes_max} (${meses_df.loc[idx_max, 'facturacion']:,.0f})")
print(f"  ↓ Peor mes:   {mes_min} (${meses_df.loc[idx_min, 'facturacion']:,.0f})")


# ── 5. Insight con pandas ─────────────────────────────────────
print("\n💡 INSIGHTS ADICIONALES (pandas)")

# Cargar todas las ventas con info de producto
df = pd.read_sql_query("""
    SELECT v.fecha, v.cantidad, v.total, p.categoria
    FROM ventas v
    JOIN productos p ON v.id_producto = p.id_producto
""", conn)

df['fecha'] = pd.to_datetime(df['fecha'])
df['dia_semana'] = df['fecha'].dt.day_name()

# Día de la semana con más ventas
ventas_por_dia = df.groupby('dia_semana')['total'].sum()
mejor_dia = ventas_por_dia.idxmax()
print(f"  Día con más ventas:   {mejor_dia}")

# Variación entre mejor y peor mes
variacion = ((meses_df['facturacion'].max() - meses_df['facturacion'].min())
             / meses_df['facturacion'].min() * 100)
print(f"  Variación estacional: {variacion:.1f}% entre mejor y peor mes")

# Participación de la categoría líder
cat_lider = categorias.iloc[0]
print(f"  Categoría líder '{cat_lider['categoria']}' concentra el {cat_lider['porcentaje']}% de la facturación")

conn.close()
print("\n" + "=" * 55)
print("  Análisis completado.")
print("=" * 55)
