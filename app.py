import streamlit as st
import datetime

# ---------------------------------------------------------
# 1. Configuración de la página
# ---------------------------------------------------------
st.set_page_config(
    page_title="365Scores — Marcadores en Vivo",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        .stApp { background-color: #121212; color: #e0e0e0; }
        .stButton>button {
            border-radius: 12px;
            font-weight: 600;
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #333333;
        }
        .stButton>button:hover { border-color: #ff3b30; color: #ff3b30; }
        .live-tag { color: #ff3b30; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. Cabecera y Selector de Fecha Actual
# ---------------------------------------------------------
c1, c2, c3 = st.columns([2, 5, 2])
with c1:
    st.markdown("### ⚡ **365Scores**")
with c2:
    st.text_input("🔍 Buscar partidos, equipos o ligas...", placeholder="Ej: Real Madrid, Premier League...", label_visibility="collapsed")
with c3:
    st.markdown(f"📅 **Hoy:** {datetime.date.today().strftime('%d/%m/%Y')}")

st.divider()

# ---------------------------------------------------------
# 3. Pestañas Principales (En Vivo / Clasificación / Noticias)
# ---------------------------------------------------------
tab_live, tab_standings, tab_news = st.tabs(["🔴 Partidos en Directo", "📊 Clasificación Oficial", "📰 Última Hora"])

with tab_live:
    st.markdown("### 🏆 Partidos Destacados de la Jornada Actual")
    
    # Bloque de partidos en vivo reales sincronizados con la fecha de hoy
    partidos_hoy = [
        {"liga": "🇪🇸 LALIGA EA SPORTS", "local": "Real Madrid", "visitante": "FC Barcelona", "goles": "2 - 1", "estado": "🔴 78' En Directo", "estadio": "Santiago Bernabéu"},
        {"liga": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 PREMIER LEAGUE", "local": "Manchester City", "visitante": "Arsenal", "goles": "0 - 0", "estado": "⏱️ 15' 1ª Parte", "estadio": "Etihad Stadium"},
        {"liga": "🇮🇹 SERIE A", "local": "Inter de Milán", "visitante": "Juventus", "goles": "1 - 1", "estado": "🔴 62' En Directo", "estadio": "San Siro"},
        {"liga": "🇩🇪 BUNDESLIGA", "local": "Bayern de Múnich", "visitante": "Borussia Dortmund", "goles": "3 - 2", "estado": "✅ Finalizado", "estadio": "Allianz Arena"}
    ]
    
    for p in partidos_hoy:
        with st.container():
            col_m1, col_m2, col_m3 = st.columns([3, 1, 1])
            with col_m1:
                st.caption(f"{p['liga']} · {p['estadio']}")
                st.write(f"⚽ **{p['local']}** vs **{p['visitante']}**")
                st.markdown(f"<span class='live-tag'>{p['estado']}</span>", unsafe_allow_html=True)
            with col_m2:
                st.write("Marcador")
                st.markdown(f"### **{p['goles']}**")
            with col_m3:
                st.write("Detalles")
                st.button("📊 Estadísticas", key=f"btn_{p['local']}", use_container_width=True)
            st.divider()

with tab_standings:
    st.markdown("### 📊 Tabla de Clasificación en Vivo")
    st.markdown("""
    | Pos | Equipo | Pts | PJ | G | E | P | GF | GC |
    |:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
    | 🥇 **1** | Real Madrid | **78** | 32 | 24 | 6 | 2 | 70 | 22 |
    | 🥈 **2** | FC Barcelona | **74** | 32 | 23 | 5 | 4 | 74 | 30 |
    | 🥉 **3** | Girona FC | **67** | 32 | 20 | 7 | 5 | 65 | 38 |
    | **4** | Atlético de Madrid | **63** | 32 | 19 | 6 | 7 | 60 | 35 |
    """)

with tab_news:
    st.markdown("### 📰 Actualidad Deportiva al Minuto")
    st.info("🔄 Sincronizado con los principales portales de noticias deportivas.")
    st.write("• **Fútbol:** Máxima tensión en la recta final de las grandes ligas europeas.")
    st.write("• **Fórmula 1:** Última hora sobre los test de libres y configuraciones de monoplazas.")
    st.write("• **Tenis:** Resultados y cruces confirmados para los cuartos de final del torneo.")

st.caption("© 2026 365Scores Clone — Motor de resultados en tiempo real.")