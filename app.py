import streamlit as st
import pandas as pd
import datetime
import sqlite3
import hashlib

# ---------------------------------------------------------
# 1. Configuración de la página (Optimizada para PWA y Móviles)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Pro | Life Control",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 2. Metaetiquetas PWA e Inyección CSS Avanzada
# ---------------------------------------------------------
st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="DashboardPro">
    <meta name="theme-color" content="#0f172a">
    <link rel="apple-touch-icon" href="https://img.icons8.com/isometric/512/dashboard.png">
    
    <style>
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 40%, #31103f 100%);
            color: #f8fafc;
        }
        .main .block-container {
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            max-width: 100% !important;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Tarjetas Neón Glassmorphism */
        .summary-card {
            background: rgba(30, 41, 59, 0.65);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            padding: 16px;
            border-radius: 18px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            margin-bottom: 12px;
            text-align: center;
        }

        .stButton>button {
            border-radius: 14px !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%) !important;
            color: white !important;
            border: none !important;
            width: 100% !important;
            min-height: 48px !important;
            margin-top: 4px;
            margin-bottom: 4px;
            box-shadow: 0 4px 15px rgba(168, 85, 247, 0.3);
        }
        .stButton>button:active { transform: scale(0.98); }

        .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input {
            border-radius: 12px !important;
            min-height: 44px !important;
            background-color: rgba(15, 23, 42, 0.6) !important;
            color: #f8fafc !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            background-color: rgba(15, 23, 42, 0.6);
            padding: 6px;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            overflow-x: auto;
            white-space: nowrap;
        }
        .stTabs [data-baseweb="tab"] {
            height: 38px;
            border-radius: 10px;
            color: #94a3b8;
            font-weight: 600;
            font-size: 0.8rem;
            padding: 0 10px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #6366f1 !important;
            color: #ffffff !important;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. Inicialización y Gestión de Base de Datos SQLite
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
    cursor.execute('''CREATE TABLE IF NOT EXISTS metas (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, meta TEXT, estado TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS habitos (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, habito TEXT, completado INTEGER, fecha TEXT)''')
    
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
# 4. Autenticación (Login / Registro)
# ---------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center; color: #a855f7; margin-top: 1rem;'>🚀 Dashboard Pro</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.9rem;'>Tu vida organizada en una sola app.</p>", unsafe_allow_html=True)
    
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
                    st.success("¡Cuenta creada! Ya puedes entrar.")
                else:
                    st.error("El usuario ya existe.")
            else:
                st.warning("Rellena todos los campos.")
    st.stop()

# ---------------------------------------------------------
# 5. Panel Principal y Navegación Modular
# ---------------------------------------------------------
user = st.session_state.username
conn = sqlite3.connect("database.db", check_same_thread=False)

col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown(f"👤 **{user}**")
with col_head2:
    if st.button("🚪 Salir", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

# Pestañas Principales (Sin Agua ni Sueño, con Hábitos)
tab_resumen, tab_diario, tab_habitos, tab_tabaco, tab_finanzas, tab_compras, tab_deporte, tab_metas = st.tabs([
    "📊 Resumen", "📖 Diario", "⚡ Hábitos", "🚬 Tabaco", "💶 Dinero", "🛒 Compra", "🏃 Deporte", "🎯 Metas"
])

# =========================================================
# SECCIÓN 1: RESUMEN GENERAL
# =========================================================
with tab_resumen:
    st.markdown("### ⚡ Visión General de tu Vida")
    
    df_fin = pd.read_sql_query("SELECT tipo, cantidad FROM finanzas WHERE username = ?", conn, params=(user,))
    df_tab = pd.read_sql_query("SELECT cigarros, gasto FROM tabaco WHERE username = ?", conn, params=(user,))
    df_metas = pd.read_sql_query("SELECT estado FROM metas WHERE username = ?", conn, params=(user,))
    df_hab = pd.read_sql_query("SELECT completado FROM habitos WHERE username = ? AND fecha = ?", conn, params=(user, str(datetime.date.today())))
    
    ingresos = df_fin[df_fin["tipo"] == "Ingreso"]["cantidad"].sum() if not df_fin.empty else 0
    gastos = df_fin[df_fin["tipo"] == "Gasto"]["cantidad"].sum() if not df_fin.empty else 0
    balance = ingresos - gastos
    
    tot_cigarros = int(df_tab["cigarros"].sum()) if not df_tab.empty else 0
    tot_gasto_tabaco = df_tab["gasto"].sum() if not df_tab.empty else 0
    metas_cumplidas = len(df_metas[df_metas["estado"] == "1"]) if not df_metas.empty else 0
    habitos_hoy = len(df_hab[df_hab["completado"] == 1]) if not df_hab.empty else 0

    c_r1, c_r2 = st.columns(2)
    with c_r1:
        st.metric("💶 Balance Neto", f"{balance:.2f} €")
        st.metric("🚬 Gasto en Tabaco", f"{tot_gasto_tabaco:.2f} €")
    with c_r2:
        st.metric("⚡ Hábitos Cumplidos Hoy", f"{habitos_hoy} listos")
        st.metric("🎯 Metas Totales", f"{metas_cumplidas} completadas")

    st.divider()
    st.caption("💡 Exportación de Copia de Seguridad:")
    if st.button("📥 Descargar Mis Finanzas (CSV)"):
        df_fin_all = pd.read_sql_query("SELECT * FROM finanzas WHERE username = ?", conn, params=(user,))
        csv = df_fin_all.to_csv(index=False).encode('utf-8')
        st.download_button("Descargar Archivo CSV", csv, "mis_finanzas.csv", "text/csv")

# =========================================================
# SECCIÓN 2: DIARIO
# =========================================================
with tab_diario:
    st.markdown("### 📖 Diario del Día")
    f_diario = st.date_input("Fecha:", datetime.date.today(), key="f_diario")
    animo = st.selectbox("Ánimo:", ["😄 Increíble", "🙂 Tranquilo", "😴 Cansado", "😤 Estresado", "💪 Motivado"])
    resumen_texto = st.text_area("¿Qué has hecho hoy?", placeholder="Resume tu día...", height=120)
    
    if st.button("💾 Guardar Entrada", use_container_width=True):
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO diario (username, fecha, animo, resumen) VALUES (?, ?, ?, ?)",
                       (user, str(f_diario), animo, resumen_texto))
        conn.commit()
        st.success("¡Guardado!")
        st.rerun()

    st.divider()
    df_diario = pd.read_sql_query("SELECT fecha as Fecha, animo as Ánimo, resumen as Resumen FROM diario WHERE username = ? ORDER BY fecha DESC", conn, params=(user,))
    if not df_diario.empty:
        for _, row in df_diario.iterrows():
            with st.expander(f"📅 {row['Fecha']} — {row['Ánimo']}"):
                st.write(row['Resumen'])
    else:
        st.info("Sin entradas guardadas.")

# =========================================================
# SECCIÓN 3: HÁBITOS DIARIOS (NUEVO)
# =========================================================
with tab_habitos:
    st.markdown("### ⚡ Rutinas y Hábitos Diarios")
    nuevo_habito = st.text_input("Añadir nuevo hábito recurrente:", placeholder="Ej: Meditar 10m, Leer 20 págs, Beber té...")
    if st.button("➕ Crear Hábito", use_container_width=True) and nuevo_habito:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO habitos (username, habito, completado, fecha) VALUES (?, ?, 0, ?)", 
                       (user, nuevo_habito, str(datetime.date.today())))
        conn.commit()
        st.rerun()

    st.divider()
    st.markdown(f"#### 📅 Hábitos para hoy: {datetime.date.today().strftime('%d/%m/%Y')}")
    df_hab = pd.read_sql_query("SELECT id, habito, completado FROM habitos WHERE username = ? AND fecha = ?", conn, params=(user, str(datetime.date.today())))
    
    if not df_hab.empty:
        for _, row in df_hab.iterrows():
            h_id = row['id']
            h_text = row['habito']
            h_state = bool(row['completado'])
            
            c_h1, c_h2 = st.columns([4, 1])
            with c_h1:
                done = st.checkbox(h_text, value=h_state, key=f"hab_{h_id}")
                if done != h_state:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE habitos SET completado = ? WHERE id = ?", (1 if done else 0, h_id))
                    conn.commit()
                    st.rerun()
            with c_h2:
                if st.button("🗑️", key=f"del_hab_{h_id}"):
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM habitos WHERE id = ?", (h_id,))
                    conn.commit()
                    st.rerun()
    else:
        st.info("No hay hábitos configurados para hoy. ¡Añade uno arriba!")

# =========================================================
# SECCIÓN 4: TABACO
# =========================================================
with tab_tabaco:
    st.markdown("### 🚬 Control de Tabaco y Ahorro")
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
        st.bar_chart(df_tab.set_index("Fecha")["Cigarros"])
    else:
        st.info("Sin registros de tabaco.")

# =========================================================
# SECCIÓN 5: FINANZAS
# =========================================================
with tab_finanzas:
    st.markdown("### 💶 Dinero Personal")
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
    df_fin_show = pd.read_sql_query("SELECT concepto as Concepto, categoria as Categoría, tipo as Tipo, cantidad as 'Cantidad (€)', fecha as Fecha FROM finanzas WHERE username = ?", conn, params=(user,))
    if not df_fin_show.empty:
        st.dataframe(df_fin_show, use_container_width=True)
    else:
        st.info("Sin movimientos financieros.")

# =========================================================
# SECCIÓN 6: COMPRAS
# =========================================================
with tab_compras:
    st.markdown("### 🛒 Lista de la Compra")
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
# SECCIÓN 7: DEPORTE
# =========================================================
with tab_deporte:
    st.markdown("### 🏃 Actividad Física")
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

# =========================================================
# SECCIÓN 8: METAS
# =========================================================
with tab_metas:
    st.markdown("### 🎯 Metas y Objetivos")
    nueva_meta = st.text_input("Nueva meta:", placeholder="Ej: Ahorrar 200€, Leer 20 min...")
    if st.button("➕ Añadir Meta", use_container_width=True) and nueva_meta:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO metas (username, meta, estado) VALUES (?, ?, 0)", (user, nueva_meta))
        conn.commit()
        st.rerun()

    st.divider()
    df_metas = pd.read_sql_query("SELECT id, meta, estado FROM metas WHERE username = ?", conn, params=(user,))
    if not df_metas.empty:
        for _, row in df_metas.iterrows():
            m_id = row['id']
            m_text = row['meta']
            m_est = bool(row['estado'])
            
            c_m1, c_m2 = st.columns([4, 1])
            with c_m1:
                completada = st.checkbox(m_text, value=m_est, key=f"meta_{m_id}")
                if completada != m_est:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE metas SET estado = ? WHERE id = ?", (1 if completada else 0, m_id))
                    conn.commit()
                    st.rerun()
            with c_m2:
                if st.button("🗑️", key=f"del_meta_{m_id}"):
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM metas WHERE id = ?", (m_id,))
                    conn.commit()
                    st.rerun()

conn.close()