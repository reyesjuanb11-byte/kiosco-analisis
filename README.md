# 📊 Análisis de Ventas — Kiosco

Proyecto de análisis de datos utilizando **Python y SQL (SQLite)**. A partir de un dataset de ventas simulado, se construye una base de datos relacional y se generan reportes con métricas clave del negocio.

---

## 🎯 Objetivo

Demostrar el uso de Python y SQL para extraer, transformar y analizar datos de ventas, identificando patrones y tendencias relevantes para la toma de decisiones.

---

## 🛠️ Tecnologías

| Herramienta | Uso |
|---|---|
| Python 3.x | Scripting y análisis |
| SQLite | Base de datos relacional embebida |
| pandas | Manipulación y análisis de datos |
| sqlite3 | Conexión y consultas SQL desde Python |

---

## 📁 Estructura del proyecto

```
kiosco-analisis/
│
├── setup_db.py      # Crea la base de datos y carga los datos de ejemplo
├── analisis.py      # Ejecuta el análisis completo con SQL + pandas
├── kiosco.db        # Base de datos generada (se crea al ejecutar setup_db.py)
└── README.md
```

---

## 🗄️ Modelo de datos

**Tabla `productos`**
| Campo | Tipo | Descripción |
|---|---|---|
| id_producto | INTEGER PK | Identificador único |
| nombre | TEXT | Nombre del producto |
| categoria | TEXT | Categoría (Bebidas, Snacks, etc.) |
| precio_unit | REAL | Precio unitario |

**Tabla `ventas`**
| Campo | Tipo | Descripción |
|---|---|---|
| id_venta | INTEGER PK | Identificador único |
| id_producto | INTEGER FK | Referencia a productos |
| fecha | TEXT | Fecha de la venta (YYYY-MM-DD) |
| cantidad | INTEGER | Unidades vendidas |
| total | REAL | Total de la transacción |

---

## 🚀 Cómo ejecutar

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu_usuario/kiosco-analisis.git
cd kiosco-analisis
```

### 2. Instalar dependencias
```bash
pip install pandas
```

### 3. Crear la base de datos
```bash
python setup_db.py
```

### 4. Ejecutar el análisis
```bash
python analisis.py
```

---

## 📈 Resultados del análisis

El script genera un reporte con:

- **Resumen general** — facturación total, ticket promedio, unidades vendidas
- **Top 5 productos** por facturación
- **Facturación por categoría** con participación porcentual
- **Evolución mensual** con identificación del mejor y peor mes
- **Insights adicionales** — día de mayor actividad, variación estacional, categoría líder

---

## 💡 Aprendizajes aplicados

- Diseño de esquema relacional con clave primaria y foránea
- Consultas SQL con `JOIN`, `GROUP BY`, `ORDER BY`, funciones de agregación
- Uso de `pandas` para análisis complementario al SQL
- Generación de datos sintéticos reproducibles con `random.seed()`

---

## 👤 Autor

**Juan Bautista Reyes**  
Estudiante de Ingeniería Informática  
[GitHub](https://github.com/tu_usuario)
