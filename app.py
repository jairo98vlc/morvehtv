import streamlit as st
import feedparser

# ---------------------------------------------------------
# 1. Configuración principal de la página
# ---------------------------------------------------------
st.set_page_config(
    page_title="MorvehTV | Canal Oficial",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ID de tu canal de YouTube
YOUTUBE_CHANNEL_ID = "UC-1WKp7GbtZUtH2FZ-XPVHg"

# Función para obtener los últimos vídeos vía RSS automáticamente (con caché)
@st.cache_data(ttl=600)  # Se actualiza automáticamente cada 10 minutos
def obtener_ultimos_videos(channel_id):
    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    feed = feedparser.parse(rss_url)
    videos = []
    for entry in feed.entries[:6]:  # Muestra los últimos 6 vídeos
        videos.append({
            "titulo": entry.title,
            "link": entry.link,
            "publicado": entry.published[:10]
        })
    return videos

# ---------------------------------------------------------
# 2. Barra Lateral (Sidebar)
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1542751371-adc38448a05e?w=500", use_container_width=True)
    st.title("📺 MorvehTV")
    st.write("¡Bienvenido a mi espacio web!")
    
    st.divider()
    
    st.markdown("### 🔗 Redes Sociales")
    st.link_button("🔴 YouTube", f"https://www.youtube.com/channel/{YOUTUBE_CHANNEL_ID}", use_container_width=True)
    st.link_button("🟣 Twitch", "https://www.twitch.tv/per3ira98", use_container_width=True)
    st.link_button("🎵 TikTok", "https://www.tiktok.com/@morvethtv", use_container_width=True)
    
    
    st.divider()
    
    st.info("⏰ **Horario habitual:**\n\nDirectos de Lunes a Viernes a las **16:00 h (España)**.")

# ---------------------------------------------------------
# 3. Encabezado y Banner Principal
# ---------------------------------------------------------
st.title("🎬 MorvehTV - Canal Oficial")
st.subheader("MotoGP streamer, Directos y videos")

st.write(
    """
    ¡Hola a todos! Bienvenidos a la web oficial de **MorvehTV**. Aquí podrás estar al día con los últimos vídeos y
    consultar los directos.
    """
)

st.divider()

# ---------------------------------------------------------
# 4. Sección Destacada (Vídeo principal + Información)
# ---------------------------------------------------------
col_main, col_stats = st.columns([2, 1])

with col_main:
    st.header("📌 Vídeo Destacado de la Semana")
    # Puedes colocar el link de tu vídeo favorito o más reciente aquí
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

with col_stats:
    st.header("🎮 Sobre el Canal")
    
    m1, m2 = st.columns(2)
    m1.metric(label="Comunidad", value="Activa")
    m2.metric(label="Calidad", value="1080p 60fps")
    
    st.markdown("""
    En **MorvehTV** nos enfocamos en:
    * 🏎️ **MotoGP 26:** Modo trayectoria.
    * 🎮 **Gaming & Directos:** Risas, gameplays e interacción con la comunidad.
    """)

st.divider()

# ---------------------------------------------------------
# 5. Sección Exclusiva: YouTube Automatizada
# ---------------------------------------------------------
st.header("🔴 Últimos Vídeos de YouTube")
st.write("Esta sección se actualiza automáticamente cada vez que publicas un nuevo vídeo en tu canal.")

try:
    videos = obtener_ultimos_videos(YOUTUBE_CHANNEL_ID)
    
    if videos:
        # Mostramos los vídeos en una cuadrícula de 2 columnas
        cols = st.columns(2)
        for index, video in enumerate(videos):
            col = cols[index % 2]
            with col:
                st.subheader(video["titulo"])
                st.caption(f"📅 Publicado el: {video['publicado']}")
                st.video(video["link"])
                st.divider()
    else:
        st.info("No se han encontrado vídeos recientes en este canal.")

except Exception as e:
    st.error("Ocurrió un error al cargar el feed de YouTube. Verifica la conexión o el ID del canal.")

st.divider()

# ---------------------------------------------------------
# 6. Formulario de Sugerencias / Contacto
# ---------------------------------------------------------
st.header("📩 ¿Qué te gustaría ver en el próximo vídeo?")
st.write("Déjame tus comentarios, ideas de vídeos o dudas técnicas aquí abajo:")

with st.form("form_sugerencias"):
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        nombre = st.text_input("Tu Nick o Nombre:")
    with col_input2:
        red_social = st.text_input("Tu Discord / Twitter (Opcional):")
        
    mensaje = st.text_area("Sugerencia o comentario:")
    enviado = st.form_submit_button("🚀 Enviar Sugerencia", use_container_width=True)
    
    if enviado:
        if nombre and mensaje:
            st.success(f"¡Muchas gracias **{nombre}**! Tu sugerencia ha sido enviada correctamente.")
        else:
            st.warning("Por favor rellena tu nombre y el mensaje antes de enviar.")

# Footer
st.markdown("---")
st.caption("© 2026 MorvehTV — Todos los derechos reservados")