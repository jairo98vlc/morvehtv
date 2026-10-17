import streamlit as st
import pandas as pd
import datetime

# ---------------------------------------------------------
# 1. Configuración de la página
# ---------------------------------------------------------
st.set_page_config(
    page_title="Mi Control Personal | Salud y Finanzas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado en modo oscuro
st.markdown("""
    <style>
        .stApp { background-color: #121212; color: #e0e0e0; }
        .metric-card {
            background-color: #1e1e1e;
            border: 1px solid #333333;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. Inicialización de la Base de Datos (Session State)
# ---------------------------------------------------------
if "registros" not in st.session_state:
    # Datos de ejemplo iniciales para visualizar los gráficos
    hoy = datetime.date.today()
    st.session_state.registros = pd.DataFrame([
        {"Fecha": hoy - datetime.timedelta(days=6), "Cigarros": 8, "Deporte": "Sí (30m Gimnasio)", "Gasto (€)": 2.40},
        {"Fecha": hoy - datetime.timedelta(days=5), "Cigarros": 6, "Deporte": "No", "Gasto (€)": 1.80},
        {"Fecha": hoy - datetime.timedelta(days=4), "Cigarros": 10, "Deporte": "Sí (45m Carrera)", "Gasto (€)": 3.00},
        {"Fecha": hoy - datetime.timedelta(days=3), "Cigarros": 5, "Deporte": "Sí (60m Bici)", "Gasto (€)": 1.50},
        {"Fecha": hoy - datetime.timedelta(days=2), "Cigarros": 7, "Deporte": "No", "Gasto (€)": 2.10},
        {"Fecha": hoy - datetime.timedelta(days=1), "Cigarros": 4, "Deporte": "Sí (40m Gimnasio)", "Gasto (€)": 1.20},
        {"Fecha": hoy, "Cigarros": 3, "Deporte": "Sí (30m Caminata)", "Gasto (€)": 0.90},
    ])

# ---------------------------------------------------------
# 3. Barra Lateral: Formulario para añadir registro diario
# ---------------------------------------------------------
with st.sidebar:
    st.header("📝 Registrar Día")
    
    fecha = st.date_input("Fecha", datetime.date.today())
    cigarros = st.number_input("Cigarros fumados:", min_value=0, max_value=100, value=5, step=1)
    
    # Precio estimado por cigarrillo (configurable)
    precio_cajetilla = st.number_input("Precio cajetilla 20 cig. (€):", min_value=1.0, max_value=20.0, value=5.0, step=0.10)
    precio_por_cigarro = precio_cajetilla / 20.0
    gasto_calculado = round(cigarros * precio_por_cigarro, 2)
    
    st.caption(f"💰 Gasto estimado hoy: **{gasto_calculado} €**")
    
    hizo_deporte = st.selectbox("¿Has hecho deporte hoy?", ["No", "Sí (Gimnasio)", "Sí (Carrera/Running)", "Sí (Ciclismo)", "Sí (Caminata)", "Sí (Otro)"])
    
    if st.button("➕ Guardar Registro", use_container_width=True, type="primary"):
        nuevo_registro = pd.DataFrame([{
            "Fecha": fecha,
            "Cigarros": cigarros,
            "Deporte": hizo_deporte,
            "Gasto (€)": gasto_calculado
        }])
        
        # Eliminar si ya existe un registro en la misma fecha y concatenar el nuevo
        st.session_state.registros = st.session_state.registros[st.session_state.registros["Fecha"] != fecha]
        st.session_state.registros = pd.concat([st.session_state.registros, nuevo_registro], ignore_index=True)
        st.session_state.registros = st.session_state.registros.sort_values(by="Fecha")
        st.success("¡Día registrado correctamente!")

# ---------------------------------------------------------
# 4. Panel Principal: Resumen Semanal y Métricas
# ---------------------------------------------------------
st.title("💪 Dashboard de Control Personal")
st.subheader("Seguimiento de hábitos, salud y finanzas")

df = st.session_state.registros.copy()

# Cálculo de totales semanales
total_cigarros = df["Cigarros"].sum()
total_gasto = round(df["Gasto (€)"].sum(), 2)
dias_deporte = len(df[df["Deporte"] != "No"])

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="🚬 Cigarros (Semana)", value=f"{total_cigarros} cig", delta=f"-{df['Cigarros'].iloc[-1]} hoy", delta_color="inverse")
with col2:
    st.metric(label="💰 Gasto Total", value=f"{total_gasto} €", delta=f"{df['Gasto (€)'].iloc[-1]} € hoy", delta_color="inverse")
with col3:
    st.metric(label="🏃 Días de Deporte", value=f"{dias_deporte} / {len(df)} días", delta="¡Sigue así!" if dias_deporte > 3 else "¡A entrenar!")

st.divider()

# ---------------------------------------------------------
# 5. Gráficos Progresivos
# ---------------------------------------------------------
tab_graficos, tab_tabla = st.tabs(["📈 Gráficos y Evolución", "📋 Historial Completo"])

with tab_graficos:
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.markdown("### 🚬 Evolución del Consumo de Tabaco")
        st.bar_chart(df.set_index("Fecha")["Cigarros"])
        
    with col_g2:
        st.markdown("### 💶 Gasto Diario en Tabaco (€)")
        st.line_chart(df.set_index("Fecha")["Gasto (€)"])

with tab_tabla:
    st.markdown("### 📜 Registros Guardados")
    st.dataframe(df.sort_values(by="Fecha", ascending=False), use_container_width=True)

st.caption("© 2026 Dashboard Personal — Control diario de hábitos.")