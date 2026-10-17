import streamlit as st
import datetime

# ---------------------------------------------------------
# 1. Configuración de la página y Estilos CSS avanzados (Modo App Móvil/Web 365Scores)
# ---------------------------------------------------------
st.set_page_config(
    page_title="365Scores — Marcadores y Resultados en Vivo",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        /* Estilo general oscuro tipo 365Scores */
        .stApp {
            background-color: #121212;
            color: #e0e0e0;
        }
        /* Botones de navegación */
        .stButton>button {
            border-radius: 12px;
            font-weight: 600;
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #333333;
        }
        .stButton>button:hover {
            border-color: #ff3b30;
            color: #ff3b30;
        }
        /* Tarjetas de partidos */
        .match-box {
            background-color: #1a1a1a;
            padding: 14px;
            border-radius: 12px;
            margin-bottom: 12px;
            border: 1px solid #2a2a2a;
        }
        .live-tag {
            color: #ff3b30;
            font-weight: bold;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.4; }
            100% { opacity: 1; }
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. Cabecera Principal y Barra de Búsqueda
# ---------------------------------------------------------
col_top1, col_top2, col_top3 = st.columns([2, 5, 2])
with col_top1:
    st.markdown("### ⚡ **365Scores**")
with col_top2:
    busqueda = st.text_input("🔍 Buscar equipo, competición o jugador...", placeholder="Ej: Real Madrid, Premier League, Alcaraz...", label_visibility="collapsed")
with col_top3:
    st.selectbox("Idioma", ["Español 🇪🇸", "English 🇬🇧"], label_visibility="collapsed")

st.divider()

# ---------------------------------------------------------
# 3. Carrusel de Fechas (Ayer, Hoy, Mañana, Selector)
# ---------------------------------------------------------
hoy = datetime.date.today()
ayer = hoy - datetime.timedelta(days=1)
mañana = hoy + datetime.timedelta(days=1)

c_f1, c_f2, c_f3, c_f4, c_f5 = st.columns(5)
with c_f1:
    if st.button(f"Ayer\n{ayer.strftime('%d/%m')}", use_container_width=True):
        st.session_state['fecha_sel'] = ayer
with c_f2:
    if st.button(f"🔥 HOY\n{hoy.strftime('%d/%m')}", use_container_width=True, type="primary"):
        st.session_state['fecha_sel'] = hoy
with c_f3:
    if st.button(f"Mañana\n{mañana.strftime('%d/%m')}", use_container_width=True):
        st.session_state['fecha_sel'] = mañana
with c_f4:
    fecha_custom = st.date_input("Elegir fecha", hoy, label_visibility="collapsed")
with c_f5:
    st.selectbox("Zona horaria", ["GMT+1 (Madrid)", "GMT-5 (Bogotá/CDMX)", "GMT-3 (Buenos Aires)"], label_visibility="collapsed")

st.divider()

# ---------------------------------------------------------
# 4. Selector de Deportes y Pestañas Principales de Navegación
# ---------------------------------------------------------
deporte = st.radio(
    "Deportes",
    ["⚽ Fútbol", "🏀 Baloncesto", "🎾 Tenis", "🏎️ F1", "🏈 NFL", "🏒 Hockey", "⚾ Béisbol"],
    horizontal=True
)

# Pestañas estilo App 365Scores
tab_partidos, tab_noticias, tab_clasificacion, tab_favoritos, tab_cuotas = st.tabs([
    "📅 Partidos", "📰 Noticias y Rumores", "📊 Clasificación", "⭐ Favoritos", "📈 Apuestas"
])

# ---------------------------------------------------------
# 5. CONTENIDO: SECCIÓN PARTIDOS
# ---------------------------------------------------------
with tab_partidos:
    
    # Filtro de estado de partidos
    sub_estado = st.selectbox(
        "Filtrar partidos:",
        ["🔴 En Directo y Próximos", "🔥 Todos en Vivo", "✅ Finalizados", "⭐ Mis Favoritos"],
        label_visibility="collapsed"
    )
    
    if deporte == "⚽ Fútbol":
        
        # --- LIGA 1: LALIGA EA SPORTS ---
        st.markdown("### 🇪🇸 **LALIGA EA SPORTS** — España")
        
        # Partido 1 (En Vivo con Expansor Detallado Completo)
        with st.container():
            col_m1, col_m2, col_m3, col_m4 = st.columns([3, 1, 1, 1])
            with col_m1:
                st.markdown("<span class='live-tag'>🔴 78' EN DIRECTO</span> · Estadio Santiago Bernabéu", unsafe_allow_html=True)
                st.write("⚪ **Real Madrid** *(Racha: 🟢 🟢 🟡 🟢 🟢)*")
                st.write("🔵🔴 **FC Barcelona** *(Racha: 🟢 🔴 🟢 🟢 🟡)*")
            with col_m2:
                st.write("")
                st.markdown("### **2**")
                st.markdown("### **1**")
            with col_m3:
                st.write("Cuotas 1X2")
                st.button("1.85", key="c_rm_1", use_container_width=True)
                st.button("3.40", key="c_rm_x", use_container_width=True)
            with col_m4:
                st.write("Acciones")
                st.button("🔔 Alerta", key="alerta_1", use_container_width=True)
                st.button("⭐ Seguir", key="fav_1", use_container_width=True)
                
            # Panel Desplegable Completo Estilo 365Scores (Centro de Partido)
            with st.expander("📊 Centro de Partido: Estadísticas, Alineaciones, Goles y Narración"):
                tab_det_1, tab_det_2, tab_det_3, tab_det_4 = st.tabs(["📌 Resumen", "📊 Estadísticas", "👥 Alineaciones", "💬 Comentarios"])
                
                with tab_det_1:
                    st.write("**Línea de Tiempo del Partido:**")
                    st.caption("⚽ 25' Gol! Vinicius Jr. (Real Madrid) asistido por F. Valverde [1-0]")
                    st.caption("🟡 34' Tarjeta amarilla para Gavi (FC Barcelona)")
                    st.caption("⚽ 40' Gol! Robert Lewandowski (FC Barcelona) [1-1]")
                    st.caption("🔄 55' Cambio en Real Madrid: Entra Modric, sale Kroos")
                    st.caption("⚽ 60' Gol! Jude Bellingham (Real Madrid) [2-1]")
                    st.caption("🔴 75' Tarjeta Roja para Ronald Araujo (FC Barcelona)")
                
                with tab_det_2:
                    st.write("**Comparativa de Estadísticas en Vivo**")
                    col_st1, col_st2, col_st3 = st.columns([2, 1, 2])
                    with col_st1:
                        st.write("52% (6)")
                        st.write("3")
                        st.write("11")
                        st.write("2")
                    with col_st2:
                        st.markdown("**Posesión**")
                        st.markdown("**Tiros a puerta**")
                        st.markdown("**Faltas**")
                        st.markdown("**Amarillas**")
                    with col_st3:
                        st.write("(4) 48%")
                        st.write("4")
                        st.write("9")
                        st.write("3")
                
                with tab_det_3:
                    st.write("**Alineaciones Iniciales (4-3-3 vs 4-4-2):**")
                    ca1, ca2 = st.columns(2)
                    with ca1:
                        st.markdown("**Real Madrid:** Courtois; Carvajal, Rüdiger, Militao, Mendy; Camavinga, Valverde, Bellingham; Vinicius, Rodrygo, Mbappé.")
                    with ca2:
                        st.markdown("**FC Barcelona:** Ter Stegen; Koundé, Cubarsí, Íñigo, Balde; De Jong, Pedri, Gavi; Lamine Yamal, Raphinha, Lewandowski.")
                
                with tab_det_4:
                    st.info("⏱️ **Minuto a minuto:** Máxima tensión en el terreno de juego. El Real Madrid defiende su ventaja con un jugador más tras la expulsión de Araujo.")

        st.divider()

        # Partido 2 (Próximo)
        col_m1, col_m2, col_m3, col_m4 = st.columns([3, 1, 1, 1])
        with col_m1:
            st.markdown("📅 **Mañana, 21:00 h** · Estadio Cívitas Metropolitano")
            st.write("🔴⚪ **Atlético de Madrid**")
            st.write("⚪🟦 **Real Sociedad**")
        with col_m2:
            st.write("")
            st.markdown("vs")
        with col_m3:
            st.write("Cuotas 1X2")
            st.button("1.95", key="c_atm_1", use_container_width=True)
            st.button("3.20", key="c_atm_x", use_container_width=True)
        with col_m4:
            st.write("Acciones")
            st.button("🔔 Alerta", key="alerta_2", use_container_width=True)
            st.button("⭐ Seguir", key="fav_2", use_container_width=True)

        st.divider()

        # --- LIGA 2: PREMIER LEAGUE ---
        st.markdown("### 🏴󠁧󠁢󠁥󠁮󠁧󠁿 **PREMIER LEAGUE** — Inglaterra")
        col_p1, col_p2, col_p3, col_p4 = st.columns([3, 1, 1, 1])
        with col_p1:
            st.markdown("<span class='live-tag'>🔴 15' 1ª PARTE</span> · Etihad Stadium", unsafe_allow_html=True)
            st.write("🔵 **Manchester City**")
            st.write("🔴 **Arsenal**")
        with col_p2:
            st.write("")
            st.markdown("### **0**")
            st.markdown("### **0**")
        with col_p3:
            st.write("Cuotas")
            st.button("2.10", key="c_mci_1", use_container_width=True)
            st.button("3.10", key="c_mci_x", use_container_width=True)
        with col_p4:
            st.write("Acciones")
            st.button("🔔 Alerta", key="alerta_3", use_container_width=True)
            st.button("⭐ Seguir", key="fav_3", use_container_width=True)

    elif deporte == "🏀 Baloncesto":
        st.markdown("### 🏀 **EUROLIGA & NBA**")
        col_b1, col_b2, col_b3 = st.columns([3, 1, 1])
        with col_b1:
            st.markdown("<span class='live-tag'>🔴 4º CUARTO (02:15)</span>", unsafe_allow_html=True)
            st.write("👑 **Real Madrid Baloncesto**")
            st.write("🔵 **Anadolu Efes**")
        with col_b2:
            st.write("")
            st.markdown("### **88**")
            st.markdown("### **84**")
        with col_b3:
            st.write("Acciones")
            st.button("📊 Ver Stats", key="stats_basket", use_container_width=True)

    elif deporte == "🏎️ F1":
        st.markdown("### 🏎️ **FÓRMULA 1 — Gran Premio en Directo**")
        st.info("🏁 **Sesión actual:** Carrera Principal — Vuelta 58 / 72")
        st.markdown("""
        | Pos | Piloto | Equipo | Neumático | Tiempo / Diferencia |
        |:---:|:---|:---|:---:|:---|
        | 🥇 **1** | Max Verstappen | Red Bull Racing | 🟡 Medium | 1:24:12.5 |
        | 🥈 **2** | Lando Norris | McLaren | ⚪ Hard | +3.2s |
        | 🥉 **3** | Charles Leclerc | Ferrari | 🟡 Medium | +7.8s |
        | **4** | Carlos Sainz | Williams | 🔴 Soft | +14.2s |
        | **5** | Fernando Alonso | Aston Martin | 🟡 Medium | +19.6s |
        """)

    else:
        st.markdown(f"### 🎯 Marcadores en vivo para {deporte}")
        st.info("Todos los partidos de la jornada se están cargando en tiempo real...")

# ---------------------------------------------------------
# 6. CONTENIDO: SECCIÓN NOTICIAS Y RUMORES
# ---------------------------------------------------------
with tab_noticias:
    st.markdown("### 📰 Últimas Noticias y Rumores de Fichajes")
    
    col_n1, col_n2 = st.columns(2)
    with col_n1:
        st.image("https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=500", use_container_width=True)
        st.subheader("🔥 ¡Bombazo en el mercado de fichajes de verano!")
        st.caption("Hace 2 horas · Fútbol Internacional")
        st.write("Las negociaciones avanzan a pasos agigantados para cerrar una de las incorporaciones más sonadas de la temporada europea.")
        st.button("Leer noticia completa", key="n1")
    
    with col_n2:
        st.image("https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=500", use_container_width=True)
        st.subheader("🏎️ Análisis previo al próximo Gran Premio")
        st.caption("Hace 4 horas · Fórmula 1")
        st.write("Los equipos traen mejoras aerodinámicas decisivas para intentar recortar distancias en el campeonato de constructores.")
        st.button("Leer noticia completa", key="n2")

# ---------------------------------------------------------
# 7. CONTENIDO: SECCIÓN CLASIFICACIÓN (STANDINGS)
# ---------------------------------------------------------
with tab_clasificacion:
    st.markdown("### 📊 Clasificación en Vivo — LALIGA EA SPORTS")
    st.markdown("""
    | Pos | Equipo | J | G | E | P | GF | GC | Pts |
    |:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
    | 🥇 **1** | Real Madrid | 32 | 24 | 6 | 2 | 70 | 22 | **78** |
    | 🥈 **2** | FC Barcelona | 32 | 23 | 5 | 4 | 74 | 30 | **74** |
    | 🥉 **3** | Girona FC | 32 | 20 | 7 | 5 | 65 | 38 | **67** |
    | **4** | Atlético de Madrid | 32 | 19 | 6 | 7 | 60 | 35 | **63** |
    | **5** | Athletic Club | 32 | 17 | 9 | 6 | 55 | 28 | **60** |
    """)

# ---------------------------------------------------------
# 8. CONTENIDO: SECCIÓN FAVORITOS Y APUESTAS
# ---------------------------------------------------------
with tab_favoritos:
    st.markdown("### ⭐ Mis Equipos y Ligas Guardadas")
    st.write("Personaliza tu experiencia seleccionando tus competiciones favoritas para acceder a ellas en un clic.")
    st.text_input("Añadir equipo o competición a favoritos:")
    st.button("💾 Guardar Preferencias", use_container_width=True)

with tab_cuotas:
    st.markdown("### 📈 Comparador de Cuotas y Estadísticas de Apuestas")
    st.info("Compara en tiempo real las mejores cuotas del mercado para tus combinadas y partidos destacados.")
    st.markdown("""
    * **Real Madrid vs FC Barcelona:** 1 (1.85) | X (3.40) | 2 (4.10)
    * **Manchester City vs Arsenal:** 1 (2.10) | X (3.10) | 2 (3.50)
    """)

# ---------------------------------------------------------
# 9. Barra de Navegación Inferior (Estilo App Móvil)
# ---------------------------------------------------------
st.markdown("---")
b_col1, b_col2, b_col3, b_col4, b_col5 = st.columns(5)
with b_col1:
    st.button("🏠 Partidos", use_container_width=True)
with b_col2:
    st.button("📰 Noticias", use_container_width=True)
with b_col3:
    st.button("📊 Tablas", use_container_width=True)
with b_col4:
    st.button("⭐ Favoritos", use_container_width=True)
with b_col5:
    st.button("⚙️ Ajustes", use_container_width=True)

st.caption("© 2026 MorvehTV — Todos los derechos reservados.")