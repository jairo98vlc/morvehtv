import streamlit as st
import pandas as pd
import datetime

# ---------------------------------------------------------
# 1. Configuración general de la página
# ---------------------------------------------------------
st.set_page_config(
    page_title="Mi Panel Personal Multisección",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo visual moderno en modo oscuro
st.markdown("""
    <style>
        .stApp { background-color: #121212; color: #e0e0e0; }
        .stButton>button { border-radius: 10px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. Inicialización de Bases de Datos en Session State
# ---------------------------------------------------------
if "tabaco_df" not in st.session_state:
    hoy = datetime.date.today()
    st.session_state.tabaco_df = pd.DataFrame([
        {"Fecha": hoy - datetime.timedelta(days=2), "Cigarros": 6, "Gasto (€)": 1.50},
        {"Fecha": hoy - datetime.timedelta(days=1), "Cigarros": 4, "Gasto (€)": 1.00},
        {"Fecha": hoy, "Cigarros": 5, "Gasto (€)": 1.25},
    ])

if "finanzas_df" not in st.session_state:
    st.session_state.finanzas_df = pd.DataFrame([
        {"Concepto": "Nómina / Ingreso", "Tipo": "Ingreso", "Cantidad (€)": 1200.0, "Fecha": str(datetime.date.today())},
        {"Concepto": "Supermercado", "Tipo": "Gasto", "Cantidad (€)": 45.50, "Fecha": str(datetime.date.today())},
        {"Concepto": "Gasolina", "Tipo": "Gasto", "Cantidad (€)": 30.0, "Fecha": str(datetime.date.today())},
    ])

if "compras_lista" not in st.session_state:
    st.session_state.compras_lista = [
        {"item": "Leche", "comprado": False},
        {"item": "Café", "comprado": True},
        {"item": "Fruta y Verdura", "comprado": False}
    ]

if "deporte_df" not in st.session_state:
    st.session_state.deporte_df = pd.DataFrame([
        {"Fecha": datetime.date.today(), "Actividad": "Gimnasio (45 min)", "Calorías": 350}
    ])

# ---------------------------------------------------------
# 3. Menú de Navegación Lateral (Secciones)
# ---------------------------------------------------------
st.sidebar.title("🗂️ Menú Principal")
seccion = st.sidebar.radio(
    "Selecciona una sección:",
    ["🚬 Control de Tabaco", "💶 Dinero Personal", "🛒 Lista de la Compra", "🏃 Deporte y Salud"]
)

st.sidebar.divider()
st.sidebar.caption("© 2026 Dashboard Personal")

# =========================================================
# SECCIÓN 1: TABACO
# =========================================================
if seccion == "🚬 Control de Tabaco":
    st.title("🚬 Control de Tabaco y Gasto")
    st.write("Registra tus consumos diarios para monitorizar tu reducción de hábitos y ahorro.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("➕ Añadir Registro Diario")
        f_tabaco = st.date_input("Fecha de hoy:", datetime.date.today(), key="f_tab")
        n_cigarros = st.number_input("Cigarros fumados:", min_value=0, max_value=100, value=4)
        precio_cajetilla = st.number_input("Precio por cajetilla (20 uds):", value=5.00)
        
        gasto_dia = round((n_cigarros / 20.0) * precio_cajetilla, 2)
        st.info(f"Gasto calculado para este día: **{gasto_dia} €**")
        
        if st.button("Guardar Consumo Tabaco", type="primary"):
            nuevo = pd.DataFrame([{"Fecha": f_tabaco, "Cigarros": n_cigarros, "Gasto (€)": gasto_dia}])
            st.session_state.tabaco_df = st.session_state.tabaco_df[st.session_state.tabaco_df["Fecha"] != f_tabaco]
            st.session_state.tabaco_df = pd.concat([st.session_state.tabaco_df, nuevo], ignore_index=True).sort_values("Fecha")
            st.success("¡Guardado correctamente!")

    with col2:
        st.subheader("📊 Resumen y Estadísticas")
        t_df = st.session_state.tabaco_df
        total_cig = t_df["Cigarros"].sum()
        total_gastado = t_df["Gasto (€)"].sum()
        
        st.metric("Total Cigarros Registrados", f"{total_cig} cig")
        st.metric("Dinero Gastado en Tabaco", f"{total_gastado:.2f} €")
        
        st.markdown("### Evolución de Cigarros")
        st.bar_chart(t_df.set_index("Fecha")["Cigarros"])

# =========================================================
# SECCIÓN 2: DINERO PERSONAL
# =========================================================
elif seccion == "💶 Dinero Personal":
    st.title("💶 Gestión de Dinero Personal")
    st.write("Controla tus ingresos y gastos semanales o mensuales.")
    
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        st.subheader("➕ Añadir Movimiento")
        concepto = st.text_input("Concepto (ej. Supermercado, Nómina):")
        tipo_mov = st.selectbox("Tipo:", ["Gasto", "Ingreso"])
        cantidad = st.number_input("Cantidad (€):", min_value=0.0, value=15.0, step=1.0)
        
        if st.button("Añadir Movimiento", type="primary"):
            nuevo_mov = pd.DataFrame([{"Concepto": concepto, "Tipo": tipo_mov, "Cantidad (€)": cantidad, "Fecha": str(datetime.date.today())}])
            st.session_state.finanzas_df = pd.concat([st.session_state.finanzas_df, nuevo_mov], ignore_index=True)
            st.success("¡Movimiento añadido!")

    with f_col2:
        st.subheader("⚖️ Balance Actual")
        fin_df = st.session_state.finanzas_df
        ingresos = fin_df[fin_df["Tipo"] == "Ingreso"]["Cantidad (€)"].sum()
        gastos = fin_df[fin_df["Tipo"] == "Gasto"]["Cantidad (€)"].sum()
        balance = ingresos - gastos
        
        st.metric("Total Ingresos", f"{ingresos:.2f} €")
        st.metric("Total Gastos", f"{gastos:.2f} €")
        st.metric("Balance Neto", f"{balance:.2f} €", delta=f"{balance} €")

    st.divider()
    st.subheader("📜 Historial de Movimientos")
    st.dataframe(fin_df, use_container_width=True)

# =========================================================
# SECCIÓN 3: LISTA DE LA COMPRA
# =========================================================
elif seccion == "🛒 Lista de la Compra":
    st.title("🛒 Lista de la Compra Interactiva")
    st.write("Añade productos pendientes y márcalos cuando los vayas comprando.")
    
    # Añadir nuevo ítem
    nuevo_item = st.text_input("Añadir producto a la lista:")
    if st.button("➕ Añadir a la lista", type="primary") and nuevo_item:
        st.session_state.compras_lista.append({"item": nuevo_item, "comprado": False})
        st.rerun()

    st.divider()
    st.subheader("📝 Productos Pendientes y Comprados")
    
    for idx, obj in enumerate(st.session_state.compras_lista):
        col_c1, col_c2 = st.columns([4, 1])
        with col_c1:
            comprado = st.checkbox(obj["item"], value=obj["comprado"], key=f"compra_{idx}")
            st.session_state.compras_lista[idx]["comprado"] = comprado
        with col_c2:
            if st.button("🗑️ Borrar", key=f"del_{idx}"):
                st.session_state.compras_lista.pop(idx)
                st.rerun()

# =========================================================
# SECCIÓN 4: DEPORTE Y SALUD
# =========================================================
elif seccion == "🏃 Deporte y Salud":
    st.title("🏃 Registro de Deporte y Actividad")
    st.write("Mantén el control de tus entrenamientos semanales.")
    
    d_col1, d_col2 = st.columns(2)
    with d_col1:
        st.subheader("➕ Registrar Actividad")
        f_dep = st.date_input("Fecha:", datetime.date.today(), key="f_dep")
        actividad = st.text_input("Actividad (ej. Running 5km, Gimnasio, Bici):")
        calorias = st.number_input("Calorías estimadas (kcal):", min_value=0, value=300, step=50)
        
        if st.button("Guardar Actividad", type="primary"):
            nuevo_dep = pd.DataFrame([{"Fecha": f_dep, "Actividad": actividad, "Calorías": calorias}])
            st.session_state.deporte_df = pd.concat([st.session_state.deporte_df, nuevo_dep], ignore_index=True)
            st.success("¡Entrenamiento registrado!")

    with d_col2:
        st.subheader("📋 Historial de Entrenos")
        st.dataframe(st.session_state.deporte_df, use_container_width=True)