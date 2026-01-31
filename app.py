import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="GraphNet Social App", layout="wide")

# Título e Introducción
st.title("🌐 GraphNet: El Recomendador de Conexiones NoSQL")
st.markdown("""
Esta aplicación demuestra cómo las bases de datos de **Grafos** gestionan relaciones 
sin necesidad de JOINs complejos. ¡Crea usuarios y conéctalos!
""")

# --- 1. GESTIÓN DEL ESTADO (Persistencia) ---
# Usamos session_state para que la red no se borre al hacer clic en botones
if 'G' not in st.session_state:
    st.session_state.G = nx.Graph()
    # Usuarios de prueba iniciales
    st.session_state.G.add_edges_from([("Alicia", "Bob"), ("Bob", "Carlos")])

# --- 2. BARRA LATERAL (Panel de Control) ---
st.sidebar.header("🛠️ Panel de Control")

# --- FUNCIONALIDAD 1: CREAR USUARIOS ---
st.sidebar.subheader("1. Registro de Usuarios")
nuevo_usuario = st.sidebar.text_input("Nombre del nuevo usuario:", placeholder="Ej: Elena")

if st.sidebar.button("Registrar en la Red"):
    if nuevo_usuario:
        if nuevo_usuario not in st.session_state.G.nodes():
            st.session_state.G.add_node(nuevo_usuario)
            st.sidebar.success(f"✅ {nuevo_usuario} se ha unido.")
        else:
            st.sidebar.warning("Este usuario ya existe.")
    else:
        st.sidebar.error("Escribe un nombre.")

st.sidebar.divider()

# --- FUNCIONALIDAD 2 Y 3: INTERACCIÓN (Crear Amistad) ---
# Decidimos la forma de interactuar: Un selector doble para conectar nodos
st.sidebar.subheader("2. Crear Interacción")
st.sidebar.caption("Define quién es amigo de quién:")

usuarios_actuales = list(st.session_state.G.nodes())

if len(usuarios_actuales) >= 2:
    u1 = st.sidebar.selectbox("Usuario Origen", usuarios_actuales, key="u1")
    u2 = st.sidebar.selectbox("Usuario Destino", usuarios_actuales, key="u2")

    if st.sidebar.button("Establecer Conexión 🤝"):
        if u1 != u2:
            st.session_state.G.add_edge(u1, u2)
            st.sidebar.balloons() # Animación de éxito
            st.sidebar.success(f"¡{u1} y {u2} ahora están conectados!")
        else:
            st.sidebar.error("Un usuario no puede conectarse consigo mismo.")
else:
    st.sidebar.info("Añade más usuarios para permitir interacciones.")

# --- 3. CUERPO PRINCIPAL (Visualización y Analítica) ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Visualización Dinámica de la Red")
    if len(st.session_state.G.nodes()) > 0:
        fig, ax = plt.subplots(figsize=(10, 7))
        # Layout circular para mejor visibilidad
        pos = nx.spring_layout(st.session_state.G, seed=42) 
        
        nx.draw(st.session_state.G, pos, with_labels=True, 
                node_color='#00d4ff', node_size=3000, 
                font_size=12, font_weight='bold', 
                edge_color='#888888', width=2)
        
        st.pyplot(fig)
    else:
        st.info("La red está vacía. Registra usuarios en la barra lateral.")

with col2:
    st.subheader("📊 Métricas Big Data")
    
    # Cálculo de influencia (Grado)
    if len(st.session_state.G.nodes()) > 0:
        grados = dict(st.session_state.G.degree())
        influencer = max(grados, key=grados.get)
        num_conexiones = grados[influencer]
        
        st.metric(label="Líder de Opinión (Influencer)", value=influencer)
        st.write(f"Este usuario tiene **{num_conexiones}** conexiones directas.")
        
        st.divider()
        st.write("**Ranking de Influencia:**")
        # Mostrar ranking simple
        for user, grado in sorted(grados.items(), key=lambda x: x[1], reverse=True):
            st.write(f"- {user}: {grado} conexiones")
    else:
        st.write("Sin datos analíticos.")
