import streamlit as st
import pandas as pd
import datetime
import sqlite3
import hashlib

# ---------------------------------------------------------
# 1. Configuración de la página (PWA & Layout Responsivo)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Life Dashboard Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 2. Inyección CSS: Diseño Dark Glassmorphism Premium
# ---------------------------------------------------------
st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="LifeDashboard">
    <meta name="theme-color" content="#0b0f19">
    <link rel="apple-touch-icon" href="https://img.icons8.com/isometric/512/dashboard.png">
    
    <style>
        .stApp {
            background: radial-gradient(circle at top right, #1e1b4b 0%, #0f172a 40%, #090d16 100%);
            color: #f8fafc;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        .main .block-container {
            padding-left: 0.85rem !important;
            padding-right: 0.85rem !important;
            padding-top: 1.2rem !important;
            padding-bottom: 2.5rem !important;
            max-width: 100% !important;
        }

        #MainMenu, footer, header { visibility: hidden; }

        .glass-card {
            background: rgba(30, 41, 59, 0.55);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            padding: 18px;
            border-radius: 20px;
            box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.4);
            margin-bottom: 14px;
        }

        .stButton>button {
            border-radius: 14px !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
            color: #ffffff !important;
            border: none !important;
            width: 100% !important;
            min-height: 48px !important;
            margin-top: 6px;
            margin-bottom: 6px;
            box-shadow: 0 4px 20px rgba(168, 85, 247, 0.35);
            transition: all 0.2s ease-in-out !important;
        }

        .stButton>button:active {
            transform: scale(0.97) !important;
            box-shadow: 0 2px 10px rgba(168, 85, 247, 0.2) !important;
        }

        .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input, .stTextArea>div>div>textarea {
            border-radius: 14px !important;
            min-height: 46px !important;
            background-color: rgba(15, 23, 42, 0.65) !important;
            color: #f8fafc !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            backdrop-filter: blur(10px);
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;
            background-color: rgba(15, 23, 42, 0.65);
            padding: 6px;
            border-radius: 18px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            overflow-x: auto;
            white-space: nowrap;
        }

        .stTabs [data-baseweb="tab"] {
            height: 42px;
            border-radius: 12px;
            color: #94a3b8;
            font-weight: 600;
            font-size: 0.85rem;
            padding: 0 14px;
            transition: all 0.2s ease;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
            color: #ffffff !important;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        }

        [data-testid="stMetricValue"] {
            font-size: 1.6rem !important;
            font-weight: 800 !important;
            color: #f8fafc !important;
        }

        @media (max-width: 640px) {
            h1 { font-size: 1.5rem !important; }
            h2 { font-size: 1.25rem !important; }
            h3 { font-size: 1.1rem !important; }
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. Base de Datos SQLite e Inicialización
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
# 4. Sistema de Autenticación
# ---------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center; color: #a855f7; margin-top: 1.5rem;'>⚡ Life Dashboard Pro</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.9rem;'>Gestión personal independiente, privada y segura.</p>", unsafe_allow_html=True)
    
    tab_log, tab_reg = st.tabs(["🔑 Acceder", "📝 Crear Cuenta"])
    
    with tab_log:
        l_user = st.text_input("Usuario", key="l_user")
        l_pass = st.text_input("Contraseña", type="password", key="l_pass")
        if st.button("Iniciar Sesión", key="btn_login", use_container_width=True):
            if verificar_usuario(l_user, l_pass):
                st.session_state.logged_in = True
                st.session_state.username = l_user
                st.success("¡Bienvenido a tu perfil privado!")
                st.rerun()
            else:
                st.error("Credenciales incorrectas.")
                
    with tab_reg:
        r_user = st.text_input("Nuevo Usuario", key="r_user")
        r_pass = st.text_input("Nueva Contraseña", type="password", key="r_pass")
        if st.button("Registrarse", key="btn_register", use_container_width=True):
            if r_user and r_pass:
                if registrar_usuario(r_user, r_pass):
                    st.success("¡Cuenta privada creada con éxito! Ya puedes iniciar sesión.")
                else:
                    st.error("El nombre de usuario ya está en uso.")
            else:
                st.warning("Completa todos los campos.")
    st.stop()

# ---------------------------------------------------------
# 5. Dashboard Principal (Aislamiento Estricto por Usuario)
# ---------------------------------------------------------
user = st.session_state.username
conn = sqlite3.connect("database.db", check_same_thread=False)

# Cabecera Privada
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown(f"👤 **Perfil Privado:** `{user}`")
with col_h2:
    if st.button("🚪 Salir", key="btn_logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

# Pestañas de Navegación
tab_resumen, tab_diario, tab_habitos, tab_tabaco, tab_finanzas, tab_compras, tab_deporte, tab_metas = st.tabs([
    "📊 Resumen", "📖 Diario", "⚡ Rutinas", "🚬 Tabaco", "💶 Dinero", "🛒 Compra", "🏃 Deporte", "🎯 Metas"
])

# =========================================================
# SECCIÓN 1: RESUMEN EJECUTIVO
# =========================================================
with tab_resumen:
    st.markdown("### 📊 Visión General de tu Perfil")
    
    df_fin = pd.read_sql_query("SELECT tipo, cantidad FROM finanzas WHERE username = ?", conn, params=(user,))
    df_tab = pd.read_sql_query("SELECT cigarros, gasto FROM tabaco WHERE username = ?", conn, params=(user,))
    df_metas = pd.read_sql_query("SELECT estado FROM metas WHERE username = ?", conn, params=(user,))
    df_hab = pd.read_sql_query("SELECT completado FROM habitos WHERE username = ? AND fecha = ?", conn, params=(user, str(datetime.date.today())))
    
    ingresos = df_fin[df_fin["tipo"] == "Ingreso"]["cantidad"].sum() if not df_fin.empty else 0.0
    gastos = df_fin[df_fin["tipo"] == "Gasto"]["cantidad"].sum() if not df_fin.empty else 0.0
    balance = ingresos - gastos
    
    tot_cig = int(df_tab["cigarros"].sum()) if not df_tab.empty else 0
    tot_gasto_tabaco = df_tab["gasto"].sum() if not df_tab.empty else 0.0
    metas_ok = len(df_metas[df_metas["estado"] == "1"]) if not df_metas.empty else 0
    habs_today = len(df_hab[df_hab["completado"] == 1]) if not df_hab.empty else 0

    c1, c2 = st.columns(2)
    with c1:
        st.metric("💶 Balance Neto", f"{balance:.2f} €")
        st.metric("🚬 Gasto Tabaco", f"{tot_gasto_tabaco:.2f} €")
    with c2:
        st.metric("⚡ Rutinas Hoy", f"{habs_today} listos")
        st.metric("🎯 Metas Cumplidas", f"{metas_ok} metas")

    st.divider()
    st.markdown("#### 📥 Copias de Seguridad Privadas")
    if st.button("Descargar Mis Finanzas (CSV)", key="btn_download_csv"):
        df_fin_all = pd.read_sql_query("SELECT * FROM finanzas WHERE username = ?", conn, params=(user,))
        csv_data = df_fin_all.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Confirmar Descarga CSV", csv_data, f"finanzas_{user}.csv", "text/csv", key="btn_confirm_dl")

# =========================================================
# SECCIÓN 2: DIARIO PERSONAL
# =========================================================
with tab_diario:
    st.markdown("### 📖 Diario Personal")
    
    with st.expander("✍️ Escribir nueva entrada", expanded=True):
        f_diario = st.date_input("Fecha:", datetime.date.today(), key="f_diario_input")
        animo = st.selectbox("Estado de ánimo:", ["😄 Increíble", "🙂 Tranquilo", "😴 Cansado", "😤 Estresado", "💪 Motivado"], key="animo_select")
        resumen_texto = st.text_area("¿Qué ha ocurrido hoy?", placeholder="Anota tus pensamientos, lecciones o logros del día...", height=120, key="diario_textarea")
        
        if st.button("💾 Guardar Entrada de Diario", key="btn_save_diario", use_container_width=True):
            if resumen_texto.strip():
                cursor = conn.cursor()
                cursor.execute("INSERT OR REPLACE INTO diario (username, fecha, animo, resumen) VALUES (?, ?, ?, ?)",
                               (user, str(f_diario), animo, resumen_texto))
                conn.commit()
                st.success("¡Entrada guardada con éxito!")
                st.rerun()
            else:
                st.warning("El texto del diario no puede estar vacío.")

    st.divider()
    st.markdown("#### 📚 Historial de Entradas")
    df_diario = pd.read_sql_query("SELECT fecha as Fecha, animo as Ánimo, resumen as Resumen FROM diario WHERE username = ? ORDER BY fecha DESC", conn, params=(user,))
    if not df_diario.empty:
        for _, row in df_diario.iterrows():
            with st.expander(f"📅 {row['Fecha']} — {row['Ánimo']}"):
                st.write(row['Resumen'])
    else:
        st.info("Aún no tienes notas guardadas en tu diario.")

# =========================================================
# SECCIÓN 3: RUTINAS Y HÁBITOS
# =========================================================
with tab_habitos:
    st.markdown("### ⚡ Hábitos y Rutinas Diarias")
    
    col_hab1, col_hab2 = st.columns([3, 1])
    with col_hab1:
        nuevo_habito = st.text_input("Nuevo hábito recurrente:", placeholder="Ej: Meditar 10m, Estudiar, Leer...", key="input_nuevo_habito")
    with col_hab2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        btn_add_hab = st.button("➕ Añadir Hábito", key="btn_add_habito", use_container_width=True)
        
    if btn_add_hab and nuevo_habito:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO habitos (username, habito, completado, fecha) VALUES (?, ?, 0, ?)", 
                       (user, nuevo_habito, str(datetime.date.today())))
        conn.commit()
        st.rerun()

    st.divider()
    st.markdown(f"#### 📅 Check-in de Hoy: {datetime.date.today().strftime('%d/%m/%Y')}")
    df_hab = pd.read_sql_query("SELECT id, habito, completado FROM habitos WHERE username = ? AND fecha = ?", conn, params=(user, str(datetime.date.today())))
    
    if not df_hab.empty:
        for _, row in df_hab.iterrows():
            h_id = row['id']
            h_text = row['habito']
            h_state = bool(row['completado'])
            
            ch1, ch2 = st.columns([4, 1])
            with ch1:
                done = st.checkbox(h_text, value=h_state, key=f"hab_{h_id}")
                if done != h_state:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE habitos SET completado = ? WHERE id = ?", (1 if done else 0, h_id))
                    conn.commit()
                    st.rerun()
            with ch2:
                if st.button("🗑️", key=f"del_hab_{h_id}"):
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM habitos WHERE id = ?", (h_id,))
                    conn.commit()
                    st.rerun()
    else:
        st.info("No hay hábitos configurados para hoy. ¡Añade uno arriba!")

# =========================================================
# SECCIÓN 4: CONTROL DE TABACO
# =========================================================
with tab_tabaco:
    st.markdown("### 🚬 Control de Tabaco y Progreso")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        f_tab = st.date_input("Fecha:", datetime.date.today(), key="f_tab_input")
        n_cig = st.number_input("Cigarros fumados:", min_value=0, value=5, key="n_cig_input")
    with col_t2:
        p_caj = st.number_input("Precio cajetilla (20 uds):", value=5.0, key="p_caj_input")
        gasto = round((n_cig / 20.0) * p_caj, 2)
        st.markdown(f"<br><b>Gasto calculado del día:</b> <span style='color: #a855f7; font-size: 1.2rem;'>{gasto:.2f} €</span>", unsafe_allow_html=True)
    
    if st.button("💾 Guardar Consumo de Tabaco", key="btn_save_tabaco", use_container_width=True):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tabaco WHERE username = ? AND fecha = ?", (user, str(f_tab)))
        cursor.execute("INSERT INTO tabaco (username, fecha, cigarros, gasto) VALUES (?, ?, ?, ?)", (user, str(f_tab), n_cig, gasto))
        conn.commit()
        st.success("¡Registro actualizado correctamente!")
        st.rerun()

    st.divider()
    st.markdown("#### 📊 Evolución Gráfica del Consumo")
    df_tab = pd.read_sql_query("SELECT fecha as Fecha, cigarros as Cigarros, gasto as 'Gasto (€)' FROM tabaco WHERE username = ? ORDER BY fecha ASC", conn, params=(user,))
    if not df_tab.empty:
        st.bar_chart(df_tab.set_index("Fecha")["Cigarros"])
        st.dataframe(df_tab, use_container_width=True)
    else:
        st.info("Sin registros de tabaco guardados todavía.")

# =========================================================
# SECCIÓN 5: FINANZAS
# =========================================================
with tab_finanzas:
    st.markdown("### 💶 Control Financiero Inteligente")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        concepto = st.text_input("Concepto del movimiento:", placeholder="Ej: Compra supermercado, Nómina...", key="fin_concepto")
        categoria = st.selectbox("Categoría:", ["🛒 Alimentación", "🏡 Hogar", "🚗 Transporte", "🎉 Ocio", "💼 Nómina", "💸 Varios"], key="fin_categoria")
    with col_f2:
        tipo = st.selectbox("Tipo:", ["Gasto", "Ingreso"], key="fin_tipo")
        cantidad = st.number_input("Cantidad (€):", min_value=0.0, value=20.0, step=5.0, key="fin_cantidad")
    
    if st.button("💾 Registrar Movimiento Financiero", key="btn_save_finanzas", use_container_width=True):
        if concepto.strip():
            cursor = conn.cursor()
            cursor.execute("INSERT INTO finanzas (username, concepto, categoria, tipo, cantidad, fecha) VALUES (?, ?, ?, ?, ?, ?)", 
                           (user, concepto, categoria, tipo, cantidad, str(datetime.date.today())))
            conn.commit()
            st.success("¡Movimiento registrado!")
            st.rerun()
        else:
            st.warning("Introduce un concepto válido.")

    st.divider()
    st.markdown("#### 📈 Historial y Análisis Financiero")
    df_fin_show = pd.read_sql_query("SELECT concepto as Concepto, categoria as Categoría, tipo as Tipo, cantidad as 'Cantidad (€)', fecha as Fecha FROM finanzas WHERE username = ?", conn, params=(user,))
    
    if not df_fin_show.empty:
        df_gastos = df_fin_show[df_fin_show["Tipo"] == "Gasto"]
        if not df_gastos.empty:
            st.markdown("##### 🔻 Gastos por Categoría")
            gastos_cat = df_gastos.groupby("Categoría")["Cantidad (€)"].sum()
            st.bar_chart(gastos_cat)
            
        st.markdown("##### 📋 Listado Completo")
        st.dataframe(df_fin_show, use_container_width=True)
    else:
        st.info("Aún no tienes movimientos financieros registrados.")

# =========================================================
# SECCIÓN 6: LISTA DE LA COMPRA
# =========================================================
with tab_compras:
    st.markdown("### 🛒 Lista de la Compra Interactiva")
    
    col_c1, col_c2 = st.columns([3, 1])
    with col_c1:
        nuevo_item = st.text_input("Añadir producto al carrito:", placeholder="Ej: Leche, Huevos, Café...", label_visibility="collapsed", key="input_nueva_compra")
    with col_c2:
        btn_add_compra = st.button("➕ Añadir Producto", key="btn_add_compra_item", use_container_width=True)
        
    if btn_add_compra and nuevo_item.strip():
        cursor = conn.cursor()
        cursor.execute("INSERT INTO compras (username, item, comprado) VALUES (?, ?, 0)", (user, nuevo_item.strip()))
        conn.commit()
        st.rerun()

    st.divider()
    df_compras = pd.read_sql_query("SELECT id, item, comprado FROM compras WHERE username = ?", conn, params=(user,))
    
    if not df_compras.empty:
        for _, row in df_compras.iterrows():
            item_id = row['id']
            item_text = row['item']
            is_bought = bool(row['comprado'])
            
            cc1, cc2 = st.columns([4, 1])
            with cc1:
                checked = st.checkbox(item_text, value=is_bought, key=f"compra_{item_id}")
                if checked != is_bought:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE compras SET comprado = ? WHERE id = ?", (1 if checked else 0, item_id))
                    conn.commit()
                    st.rerun()
            with cc2:
                if st.button("🗑️", key=f"del_compra_{item_id}"):
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM compras WHERE id = ?", (item_id,))
                    conn.commit()
                    st.rerun()
    else:
        st.info("Tu lista de la compra está vacía.")

# =========================================================
# SECCIÓN 7: DEPORTE
# =========================================================
with tab_deporte:
    st.markdown("### 🏃 Actividad Física y Deporte")
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        f_dep = st.date_input("Fecha:", datetime.date.today(), key="f_dep_input")
        act = st.text_input("Actividad:", placeholder="Ej: Gimnasio, Running, Ciclismo", key="actividad_input")
    with col_d2:
        cal = st.number_input("Calorías estimadas (kcal):", min_value=0, value=300, step=50, key="cal_input")
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        
    if st.button("💾 Guardar Entrenamiento", key="btn_save_deporte", use_container_width=True):
        if act.strip():
            cursor = conn.cursor()
            cursor.execute("INSERT INTO deporte (username, fecha, actividad, calorias) VALUES (?, ?, ?, ?)", (user, str(f_dep), act, cal))
            conn.commit()
            st.success("¡Entrenamiento guardado con éxito!")
            st.rerun()
        else:
            st.warning("Introduce el nombre de la actividad.")

    st.divider()
    st.markdown("#### 📋 Historial de Entrenamientos")
    df_dep = pd.read_sql_query("SELECT fecha as Fecha, actividad as Actividad, calorias as 'Calorías (kcal)' FROM deporte WHERE username = ? ORDER BY fecha DESC", conn, params=(user,))
    if not df_dep.empty:
        st.dataframe(df_dep, use_container_width=True)
    else:
        st.info("Sin entrenamientos registrados.")

# =========================================================
# SECCIÓN 8: METAS Y OBJETIVOS
# =========================================================
with tab_metas:
    st.markdown("### 🎯 Metas y Objetivos Personales")
    
    col_m1, col_m2 = st.columns([3, 1])
    with col_m1:
        nueva_meta = st.text_input("Nueva meta:", placeholder="Ej: Ahorrar 500€, Leer 5 libros...", label_visibility="collapsed", key="input_nueva_meta")
    with col_m2:
        btn_add_meta = st.button("➕ Crear Meta", key="btn_add_meta_item", use_container_width=True)
        
    if btn_add_meta and nueva_meta.strip():
        cursor = conn.cursor()
        cursor.execute("INSERT INTO metas (username, meta, estado) VALUES (?, ?, '0')", (user, nueva_meta.strip()))
        conn.commit()
        st.rerun()

    st.divider()
    st.markdown("#### 🏆 Tus Objetivos Activos")
    df_metas = pd.read_sql_query("SELECT id, meta, estado FROM metas WHERE username = ?", conn, params=(user,))
    
    if not df_metas.empty:
        for _, row in df_metas.iterrows():
            m_id = row['id']
            m_text = row['meta']
            m_est = True if str(row['estado']) == '1' else False
            
            cm1, cm2, cm3 = st.columns([3, 1, 1])
            with cm1:
                completada = st.checkbox(m_text, value=m_est, key=f"meta_{m_id}")
                if completada != m_est:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE metas SET estado = ? WHERE id = ?", ('1' if completada else '0', m_id))
                    conn.commit()
                    st.rerun()
            with cm2:
                if completada:
                    st.markdown("<span style='color: #4ade80; font-weight: 700;'>✅ Completada</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span style='color: #facc15; font-weight: 600;'>⏳ Pendiente</span>", unsafe_allow_html=True)
            with cm3:
                if st.button("🗑️ Borrar", key=f"del_meta_{m_id}"):
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM metas WHERE id = ?", (m_id,))
                    conn.commit()
                    st.rerun()
    else:
        st.info("No tienes metas registradas. ¡Añade tu primer objetivo arriba!")

conn.close()