import streamlit as st
import pandas as pd
import datetime
import sqlite3
import hashlib

# ---------------------------------------------------------
# 1. Configuración de la página
# ---------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Pro | Control Total",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. Estilos CSS: Fondo llamativo (Gradiente y Neón / Glassmorphism)
# ---------------------------------------------------------
st.markdown("""
    <style>
        /* Fondo general con degradado llamativo */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #31103f 100%);
            color: #f8fafc;
        }
        /* Tarjetas estilo Glassmorphism */
        .metric-card {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }
        /* Botones personalizados */
        .stButton>button {
            border-radius: 12px;
            font-weight: 700;
            background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
            color: white;
            border: none;
            transition: 0.3s;
        }
        .stButton>button:hover {
            transform: scale(1.02);
            box-shadow: 0 0 15px rgba(168, 85, 247, 0.6);
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. Base de Datos SQLite (Usuarios y Datos Persistentes)
# ---------------------------------------------------------
def init_db():
    conn = sqlite3.connect("database.db", check_same_thread=False)
    cursor = conn.cursor()
    # Tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    # Tabla de tabaco
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tabaco (
            username TEXT,
            fecha TEXT,
            cigarros INTEGER,
            gasto REAL
        )
    ''')
    # Tabla de finanzas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS finanzas (
            username TEXT,
            concepto TEXT,
            tipo TEXT,
            cantidad REAL,
            fecha TEXT
        )
    ''')
    # Tabla de deporte
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deporte (
            username TEXT,
            fecha TEXT,
            actividad TEXT,
            calorias INTEGER
        )
    ''')
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
# 4. Sistema de Autenticación (Login / Registro)
# ---------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #a855f7;'>🚀 Panel Personal Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Inicia sesión o regístrate para acceder a tus datos seguros.</p>", unsafe_allow_html=True)
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        tab_log, tab_reg = st.tabs(["🔑 Iniciar Sesión", "📝 Registrarse"])
        
        with tab_log:
            l_user = st.text_input("Usuario", key="l_user")
            l_pass = st.text_input("Contraseña", type="password", key="l_pass")
            if st.button("Entrar", use_container_width=True):
                if verificar_usuario(l_user, l_pass):
                    st.session_state.logged_in = True
                    st.session_state.username = l_user
                    st.success("¡Bienvenido de nuevo!")
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos.")
                    
        with tab_reg:
            r_user = st.text_input("Nuevo Usuario", key="r_user")
            r_pass = st.text_input("Nueva Contraseña", type="password", key="r_pass")
            if st.button("Crear Cuenta", use_container_width=True):
                if r_user and r_pass:
                    if registrar_usuario(r_user, r_pass):
                        st.success("¡Cuenta creada con éxito! Ya puedes iniciar sesión.")
                    else:
                        st.error("El usuario ya existe.")
                else:
                    st.warning("Rellena todos los campos.")
    st.stop()

# ---------------------------------------------------------
# 5. Dashboard Principal (Usuario Autenticado)
# ---------------------------------------------------------
user = st.session_state.username

st.sidebar.title(f"👤 Hola, {user}")
if st.sidebar.button("🚪 Cerrar Sesión"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

st.sidebar.divider()
seccion = st.sidebar.radio(
    "Menú de Navegación",
    ["🚬 Control de Tabaco", "💶 Dinero Personal", "🏃 Deporte y Salud"]
)

# Conexión activa para consultas de usuario
conn = sqlite3.connect("database.db", check_same_thread=False)

# =========================================================
# SECCIÓN 1: TABACO
# =========================================================
if seccion == "🚬 Control de Tabaco":
    st.title("🚬 Control de Tabaco en Tiempo Real")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("➕ Registrar Consumo")
        f_tab = st.date_input("Fecha:", datetime.date.today())
        n_cig = st.number_input("Cigarros fumados:", min_value=0, value=5)
        p_caj = st.number_input("Precio cajetilla (20 uds):", value=5.0)
        gasto = round((n_cig / 20.0) * p_caj, 2)
        
        if st.button("Guardar en vivo", type="primary"):
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tabaco WHERE username = ? AND fecha = ?", (user, str(f_tab)))
            cursor.execute("INSERT INTO tabaco (username, fecha, cigarros, gasto) VALUES (?, ?, ?, ?)", (user, str(f_tab), n_cig, gasto))
            conn.commit()
            st.success("¡Actualizado al instante!")
            st.rerun()

    with c2:
        st.subheader("📊 Tus Estadísticas")
        df_tab = pd.read_sql_query("SELECT fecha as Fecha, cigarros as Cigarros, gasto as 'Gasto (€)' FROM tabaco WHERE username = ?", conn, params=(user,))
        if not df_tab.empty:
            st.metric("Total Cigarros", int(df_tab["Cigarros"].sum()))
            st.metric("Gasto Total", f"{df_tab['Gasto (€)'].sum():.2f} €")
            st.bar_chart(df_tab.set_index("Fecha")["Cigarros"])
        else:
            st.info("No hay registros todavía.")

# =========================================================
# SECCIÓN 2: DINERO PERSONAL
# =========================================================
elif seccion == "💶 Dinero Personal":
    st.title("💶 Control Financiero en Tiempo Real")
    
    d1, d2 = st.columns(2)
    with d1:
        st.subheader("➕ Añadir Movimiento")
        concepto = st.text_input("Concepto:")
        tipo = st.selectbox("Tipo:", ["Gasto", "Ingreso"])
        cantidad = st.number_input("Cantidad (€):", min_value=0.0, value=20.0)
        
        if st.button("Añadir Movimiento", type="primary"):
            cursor = conn.cursor()
            cursor.execute("INSERT INTO finanzas (username, concepto, tipo, cantidad, fecha) VALUES (?, ?, ?, ?, ?)", 
                           (user, concepto, tipo, cantidad, str(datetime.date.today())))
            conn.commit()
            st.success("¡Movimiento registrado al instante!")
            st.rerun()

    with d2:
        st.subheader("⚖️ Balance")
        df_fin = pd.read_sql_query("SELECT concepto as Concepto, tipo as Tipo, cantidad as 'Cantidad (€)', fecha as Fecha FROM finanzas WHERE username = ?", conn, params=(user,))
        if not df_fin.empty:
            ingresos = df_fin[df_fin["Tipo"] == "Ingreso"]["Cantidad (€)"].sum()
            gastos = df_fin[df_fin["Tipo"] == "Gasto"]["Cantidad (€)"].sum()
            balance = ingresos - gastos
            st.metric("Balance Neto", f"{balance:.2f} €")
            st.dataframe(df_fin, use_container_width=True)
        else:
            st.info("Aún no hay movimientos registrados.")

# =========================================================
# SECCIÓN 3: DEPORTE Y SALUD
# =========================================================
elif seccion == "🏃 Deporte y Salud":
    st.title("🏃 Registro de Actividad Física")
    
    s1, s2 = st.columns(2)
    with s1:
        st.subheader("➕ Añadir Actividad")
        f_dep = st.date_input("Fecha:", datetime.date.today(), key="fd")
        act = st.text_input("Actividad (Ej: Gimnasio, Running):")
        cal = st.number_input("Calorías (kcal):", min_value=0, value=300)
        
        if st.button("Guardar Actividad", type="primary"):
            cursor = conn.cursor()
            cursor.execute("INSERT INTO deporte (username, fecha, actividad, calorias) VALUES (?, ?, ?, ?)", (user, str(f_dep), act, cal))
            conn.commit()
            st.success("¡Entreno guardado!")
            st.rerun()

    with s2:
        st.subheader("📜 Tus Entrenamientos")
        df_dep = pd.read_sql_query("SELECT fecha as Fecha, actividad as Actividad, calorias as Calorías FROM deporte WHERE username = ?", conn, params=(user,))
        if not df_dep.empty:
            st.dataframe(df_dep, use_container_width=True)
        else:
            st.info("Sin registros de deporte todavía.")

conn.close()