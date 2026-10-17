import streamlit as st
import pandas as pd
import datetime
import sqlite3
import hashlib

# ---------------------------------------------------------
# 1. Configuración de la página (Optimizada para PWA)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Pro",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 2. Metaetiquetas PWA e Inyección HTML para iPhone y Android
# ---------------------------------------------------------
pwa_meta_tags = """
    <!-- Metaetiquetas para hacerlo PWA Instalable en iOS / Android -->
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="DashboardPro">
    <meta name="theme-color" content="#0f172a">
    <link rel="apple-touch-icon" href="https://img.icons8.com/isometric/512/dashboard.png">
    
    <!-- Manifiesto PWA Web App -->
    <link rel="manifest" href="data:application/json;base64,ewogICJuYW1lIjogIkRhc2hib2FyZCBQcm8gRGFpbHkiLAogICJzaG9ydF9uYW1lIjogIkRhc2hib2FyZFAiLAogICJzdGFydF91cmwiOiAiLi8iLAogICJkaXNwbGF5IjogInN0YW5kYWxvbmUiLAogICJiYWNrZ3JvdW5kX2NvbG9yIjogIiMwZjE3MmEiLAogICJ0aGVtZV9jb2xvciI6ICIjMGYxNzJhIiwKICAiaWNvbnMiOiBbCiAgICB7CiAgICAgICJzcmMiOiAiaHR0cHM6Ly9pbWcuaWNvbnM4LmNvbS9pc29tZXRyaWMvNTEyL2Rhc2hib2FyZC5wbmciLAogICAgICAic2l6ZXMiOiAiNTEyeDUxMiIsCiAgICAgICJ0eXBlIjogImltYWdlL3BuZyIKICAgIH0KICBdCn0=">
"""

st.markdown(pwa_meta_tags, unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. Estilos CSS Avanzados
# ---------------------------------------------------------
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 40%, #31103f 100%);
            color: #f8fafc;
        }
        .metric-card {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 14px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            margin-bottom: 10px;
        }
        .stButton>button {
            border-radius: 12px;
            font-weight: 700;
            background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
            color: white;
            border: none;
            width: 100%;
            padding: 0.5rem 1rem;
            transition: 0.3s;
        }
        .stButton>button:hover {
            transform: scale(1.01);
            box-shadow: 0 0 12px rgba(168, 85, 247, 0.6);
        }
        @media (max-width: 640px) {
            h1 { font-size: 1.6rem !important; }
            h2 { font-size: 1.3rem !important; }
            h3 { font-size: 1.1rem !important; }
            .block-container {
                padding-left: 1rem !important;
                padding-right: 1rem !important;
                padding-top: 1.5rem !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. Inicialización y Base de Datos SQLite
# ---------------------------------------------------------
def init_db():
    conn = sqlite3.connect("database.db", check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS tabaco (username TEXT, fecha TEXT, cigarros INTEGER, gasto REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS finanzas (username TEXT, concepto TEXT, categoria TEXT, tipo TEXT, cantidad REAL, fecha TEXT)''')
    
    cursor.execute("PRAGMA table_info(finanzas)")
    columnas = [info[1] for info in cursor.fetchall()]
    if "categoria" not in columnas:
        cursor.execute("ALTER TABLE finanzas ADD COLUMN categoria TEXT DEFAULT 'Varios'")

    cursor.execute('''CREATE TABLE IF NOT EXISTS compras (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, item TEXT, comprado INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS diario (username TEXT, fecha TEXT, animo TEXT, resumen TEXT, PRIMARY KEY (username, fecha))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS deporte (username TEXT, fecha TEXT, actividad TEXT, calorias INTEGER)''')
    
    conn.commit()
    conn.close()

init_db()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def registrar_usuario(username, password):
    conn = sqlite3.connect("database.db", check_same_thread=False)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

def verificar_usuario(username, password):
    conn = sqlite3.connect("database.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row and row[0] == hash_password(password):
        return True
    return False

# ---------------------------------------------------------
# 5. Autenticación (Login / Registro)
# ---------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #a855f7;'>📱 Dashboard Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Inicia sesión para gestionar tus datos guardados.</p>", unsafe_allow_html=True)
    
    col_l1, col_l2, col_l3 = st.columns([0.1, 2, 0.1])
    with col_l2:
        tab_log, tab_reg = st.tabs(["🔑 Entrar", "📝 Registro"])
        
        with tab_log:
            l_user = st.text_input("Usuario", key="l_user")
            l_pass = st.text_input("Contraseña", type="password", key="l_pass")
            if st.button("Iniciar Sesión", use_container_width=True):
                if verificar_usuario(l_user, l_pass):
                    st.session_state.logged_in = True
                    st.session_state.username = l_user
                    st.success("¡Acceso concedido!")
                    st.rerun()
                else:
                    st.error("Datos incorrectos.")
                    
        with tab_reg:
            r_user = st.text_input("Nuevo Usuario", key="r_user")
            r_pass = st.text_input("Nueva Contraseña", type="password", key="r_pass")
            if st.button("Registrarse", use_container_width=True):
                if r_user and r_pass:
                    if registrar_usuario(r_user, r_pass):
                        st.success("¡Cuenta creada! Ya puedes iniciar sesión.")
                    else:
                        st.error("El usuario ya existe.")
                else:
                    st.warning("Rellena todos los campos.")
    st.stop()

# ---------------------------------------------------------
# 6. Panel Principal
# ---------------------------------------------------------
user = st.session_state.username
conn = sqlite3.connect("database.db", check_same_thread=False)

st.sidebar.title(f"👤 Hola, {user}")
if st.sidebar.button("🚪 Cerrar Sesión", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

st.sidebar.divider()
seccion = st.sidebar.radio(
    "Menú de Navegación",
    ["📖 Diario Personal", "🚬 Tabaco", "💶 Finanzas", "🛒 Compras", "🏃 Deporte"]
)

# =========================================================
# SECCIÓN 1: DIARIO
# =========================================================
if seccion == "📖 Diario Personal":
    st.title("📖 Diario del Día")
    
    f_diario = st.date_input("Fecha:", datetime.date.today(), key="f_diario")
    animo = st.selectbox("Ánimo:", ["😄 Increíble", "🙂 Tranquilo", "😴 Cansado", "😤 Estresado", "💪 Motivado"])
    resumen_texto = st.text_area("¿Qué has hecho hoy?", placeholder="Resume tu día...")
    
    if st.button("💾 Guardar Entrada", use_container_width=True):
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO diario (username, fecha, animo, resumen) VALUES (?, ?, ?, ?)",
                       (user, str(f_diario), animo, resumen_texto))
        conn.commit()
        st.success("¡Guardado!")
        st.rerun()

    st.divider()
    st.subheader("📜 Entradas Recientes")
    df_diario = pd.read_sql_query("SELECT fecha as Fecha, animo as Ánimo, resumen as Resumen FROM diario WHERE username = ? ORDER BY fecha DESC", conn, params=(user,))
    if not df_diario.empty:
        for _, row in df_diario.iterrows():
            with st.expander(f"📅 {row['Fecha']} — {row['Ánimo']}"):
                st.write(row['Resumen'])
    else:
        st.info("Sin entradas guardadas.")

# =========================================================
# SECCIÓN 2: TABACO
# =========================================================
elif seccion == "🚬 Tabaco":
    st.title("🚬 Control de Tabaco")
    
    f_tab = st.date_input("Fecha:", datetime.date.today(), key="f_tab")
    n_cig = st.number_input("Cigarros fumados:", min_value=0, value=5)
    p_caj = st.number_input("Precio cajetilla (20 uds):", value=5.0)
    gasto = round((n_cig / 20.0) * p_caj, 2)
    
    if st.button("Guardar Consumo", use_container_width=True):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tabaco WHERE username = ? AND fecha = ?", (user, str(f_tab)))
        cursor.execute("INSERT INTO tabaco (username, fecha, cigarros, gasto) VALUES (?, ?, ?, ?)", (user, str(f_tab), n_cig, gasto))
        conn.commit()
        st.success("¡Actualizado!")
        st.rerun()

    st.divider()
    df_tab = pd.read_sql_query("SELECT fecha as Fecha, cigarros as Cigarros, gasto as 'Gasto (€)' FROM tabaco WHERE username = ? ORDER BY fecha ASC", conn, params=(user,))
    if not df_tab.empty:
        st.metric("Total Cigarros", int(df_tab["Cigarros"].sum()))
        st.metric("Gasto Total", f"{df_tab['Gasto (€)'].sum():.2f} €")
        st.bar_chart(df_tab.set_index("Fecha")["Cigarros"])
    else:
        st.info("Sin registros de tabaco.")

# =========================================================
# SECCIÓN 3: FINANZAS
# =========================================================
elif seccion == "💶 Finanzas":
    st.title("💶 Dinero Personal")
    
    concepto = st.text_input("Concepto:")
    categoria = st.selectbox("Categoría:", ["🛒 Alimentación", "🏡 Hogar", "🚗 Transporte", "🎉 Ocio", "💼 Nómina", "💸 Varios"])
    tipo = st.selectbox("Tipo:", ["Gasto", "Ingreso"])
    cantidad = st.number_input("Cantidad (€):", min_value=0.0, value=20.0)
    
    if st.button("Registrar Movimiento", use_container_width=True):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO finanzas (username, concepto, categoria, tipo, cantidad, fecha) VALUES (?, ?, ?, ?, ?, ?)", 
                       (user, concepto, categoria, tipo, cantidad, str(datetime.date.today())))
        conn.commit()
        st.success("¡Registrado!")
        st.rerun()

    st.divider()
    df_fin = pd.read_sql_query("SELECT concepto as Concepto, categoria as Categoría, tipo as Tipo, cantidad as 'Cantidad (€)', fecha as Fecha FROM finanzas WHERE username = ?", conn, params=(user,))
    if not df_fin.empty:
        ingresos = df_fin[df_fin["Tipo"] == "Ingreso"]["Cantidad (€)"].sum()
        gastos = df_fin[df_fin["Tipo"] == "Gasto"]["Cantidad (€)"].sum()
        balance = ingresos - gastos
        
        st.metric("Balance Neto", f"{balance:.2f} €")
        st.dataframe(df_fin, use_container_width=True)
    else:
        st.info("Sin movimientos financieros.")

# =========================================================
# SECCIÓN 4: COMPRAS
# =========================================================
elif seccion == "🛒 Compras":
    st.title("🛒 Lista de la Compra")
    
    nuevo_item = st.text_input("Añadir producto:", placeholder="Ej: Leche, Huevos...")
    if st.button("➕ Añadir a la lista", use_container_width=True) and nuevo_item:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO compras (username, item, comprado) VALUES (?, ?, 0)", (user, nuevo_item))
        conn.commit()
        st.rerun()

    st.divider()
    df_compras = pd.read_sql_query("SELECT id, item, comprado FROM compras WHERE username = ?", conn, params=(user,))
    
    if not df_compras.empty:
        for _, row in df_compras.iterrows():
            item_id = row['id']
            item_text = row['item']
            is_bought = bool(row['comprado'])
            
            c_check, c_del = st.columns([4, 1])
            with c_check:
                checked = st.checkbox(item_text, value=is_bought, key=f"compra_{item_id}")
                if checked != is_bought:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE compras SET comprado = ? WHERE id = ?", (1 if checked else 0, item_id))
                    conn.commit()
                    st.rerun()
            with c_del:
                if st.button("🗑️", key=f"del_{item_id}"):
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM compras WHERE id = ?", (item_id,))
                    conn.commit()
                    st.rerun()
    else:
        st.info("La lista está vacía.")

# =========================================================
# SECCIÓN 5: DEPORTE
# =========================================================
elif seccion == "🏃 Deporte":
    st.title("🏃 Actividad Física")
    
    f_dep = st.date_input("Fecha:", datetime.date.today(), key="fd")
    act = st.text_input("Actividad (Ej: Gimnasio, Bici):")
    cal = st.number_input("Calorías (kcal):", min_value=0, value=300)
    
    if st.button("Guardar Entreno", use_container_width=True):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO deporte (username, fecha, actividad, calorias) VALUES (?, ?, ?, ?)", (user, str(f_dep), act, cal))
        conn.commit()
        st.success("¡Entreno guardado!")
        st.rerun()

    st.divider()
    df_dep = pd.read_sql_query("SELECT fecha as Fecha, actividad as Actividad, calorias as 'Calorías (kcal)' FROM deporte WHERE username = ?", conn, params=(user,))
    if not df_dep.empty:
        st.dataframe(df_dep, use_container_width=True)
    else:
        st.info("Sin entrenamientos registrados.")

conn.close()