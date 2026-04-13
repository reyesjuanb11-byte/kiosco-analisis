"""
analisis.py
Análisis de ventas del kiosco usando SQL + pandas + matplotlib.
Requiere haber ejecutado setup_db.py primero.
"""
 
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os
 
DB_PATH = "kiosco.db"
OUTPUT_DIR = "graficos"
os.makedirs(OUTPUT_DIR, exist_ok=True)
 
plt.rcParams.update({
    "figure.facecolor": "#1e1e2e",
    "axes.facecolor":   "#1e1e2e",
    "axes.edgecolor":   "#444",
    "axes.labelcolor":  "#ccc",
    "text.color":       "#eee",
    "xtick.color":      "#ccc",
    "ytick.color":      "#ccc",
    "grid.color":       "#333",
    "font.family":      "sans-serif",
    "font.size":        11,
})
 
conn = sqlite3.connect(DB_PATH)
 
print("=" * 55)
print("   ANÁLISIS DE VENTAS — KIOSCO 2024")
print("=" * 55)
 
query_resumen = """
    SELECT COUNT(*) AS total_transacciones, SUM(total) AS facturacion_total,
           ROUND(AVG(total), 2) AS ticket_promedio, SUM(cantidad) AS unidades_vendidas
    FROM ventas;
"""
resumen = pd.read_sql_query(query_resumen, conn).iloc[0]
print(f"\n📊 RESUMEN GENERAL")
print(f"  Transacciones:      {int(resumen['total_transacciones']):,}")
print(f"  Facturación total:  ${resumen['facturacion_total']:,.0f}")
print(f"  Ticket promedio:    ${resumen['ticket_promedio']:,.2f}")
print(f"  Unidades vendidas:  {int(resumen['unidades_vendidas']):,}")
 
query_top = """
    SELECT p.nombre, SUM(v.total) AS facturacion, SUM(v.cantidad) AS unidades
    FROM ventas v JOIN productos p ON v.id_producto = p.id_producto
    GROUP BY p.id_producto ORDER BY facturacion DESC LIMIT 5;
"""
top_productos = pd.read_sql_query(query_top, conn)
 
query_cat = """
    SELECT p.categoria, SUM(v.total) AS facturacion,
           ROUND(SUM(v.total)*100.0/(SELECT SUM(total) FROM ventas),1) AS porcentaje
    FROM ventas v JOIN productos p ON v.id_producto = p.id_producto
    GROUP BY p.categoria ORDER BY facturacion DESC;
"""
categorias = pd.read_sql_query(query_cat, conn)
 
query_mes = """
    SELECT strftime('%m', fecha) AS mes, SUM(total) AS facturacion
    FROM ventas GROUP BY mes ORDER BY mes;
"""
meses_df = pd.read_sql_query(query_mes, conn)
MESES = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
meses_df["nombre"] = meses_df["mes"].apply(lambda x: MESES[int(x)-1])
idx_max = meses_df["facturacion"].idxmax()
idx_min = meses_df["facturacion"].idxmin()
 
conn.close()
 
AZUL    = "#4C9BE8"
VERDE   = "#56D98A"
COLORES = ["#4C9BE8","#56D98A","#F4A940","#E05C7A","#A77BF3","#4DD9C0"]
 
# Gráfico 1: Facturación mensual
fig, ax = plt.subplots(figsize=(11, 5))
bars = ax.bar(meses_df["nombre"], meses_df["facturacion"], color=AZUL, width=0.6, zorder=3)
bars[idx_max].set_color(VERDE)
bars[idx_min].set_color("#E05C7A")
ax.set_title("Facturación mensual — Kiosco 2024", fontsize=14, fontweight="bold", pad=15)
ax.set_ylabel("Facturación ($)", labelpad=10)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.grid(axis="y", zorder=0)
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x()+bar.get_width()/2, h+800, f"${h:,.0f}", ha="center", va="bottom", fontsize=8.5, color="#ccc")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=VERDE,label="Mejor mes"),Patch(color="#E05C7A",label="Peor mes"),Patch(color=AZUL,label="Resto")], loc="upper left", framealpha=0.2)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR,"01_facturacion_mensual.png"), dpi=150, bbox_inches="tight")
plt.show()
print("\n✅ Gráfico 1 guardado: graficos/01_facturacion_mensual.png")
 
# Gráfico 2: Torta por categoría
fig, ax = plt.subplots(figsize=(8, 6))
wedges, texts, autotexts = ax.pie(categorias["facturacion"], labels=categorias["categoria"],
    autopct="%1.1f%%", colors=COLORES[:len(categorias)], startangle=140,
    wedgeprops={"linewidth":1.5,"edgecolor":"#1e1e2e"}, pctdistance=0.75)
for t in autotexts:
    t.set_fontsize(10); t.set_color("white"); t.set_fontweight("bold")
ax.set_title("Participación por categoría", fontsize=14, fontweight="bold", pad=15)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR,"02_categorias.png"), dpi=150, bbox_inches="tight")
plt.show()
print("✅ Gráfico 2 guardado: graficos/02_categorias.png")
 
# Gráfico 3: Top 5 horizontal
fig, ax = plt.subplots(figsize=(9, 5))
bars_h = ax.barh(top_productos["nombre"][::-1], top_productos["facturacion"][::-1],
                 color=COLORES[:len(top_productos)][::-1], height=0.55, zorder=3)
ax.set_title("Top 5 productos por facturación", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Facturación ($)", labelpad=10)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.grid(axis="x", zorder=0)
for bar in bars_h:
    w = bar.get_width()
    ax.text(w+3000, bar.get_y()+bar.get_height()/2, f"${w:,.0f}", va="center", fontsize=9, color="#ccc")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR,"03_top_productos.png"), dpi=150, bbox_inches="tight")
plt.show()
print("✅ Gráfico 3 guardado: graficos/03_top_productos.png")
 
print("\n" + "=" * 55)
print("  Análisis completado. Gráficos en carpeta /graficos")
print("=" * 55)
 