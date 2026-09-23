import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="Monitor de Ciclo Económico e Inversiones",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Monitor del Ciclo Económico e Inversión Estratégica")
st.write("Herramienta interactiva para diagnosticar la fase del ciclo económico según indicadores clave y determinar la distribución óptima de activos.")

# Barra lateral para capturar los indicadores
st.sidebar.header("📊 Indicadores Macroeconómicos")
st.sidebar.write("Ajusta los valores según los datos actuales:")

pib = st.sidebar.slider("Crecimiento del PIB Anual (%)", min_value=-5.0, max_value=8.0, value=1.0, step=0.1)
inflacion = st.sidebar.slider("Inflación General (%)", min_value=0.0, max_value=15.0, value=3.3, step=0.1)
tasa_banxico = st.sidebar.slider("Tasa de Referencia Banxico (%)", min_value=2.0, max_value=15.0, value=6.5, step=0.25)
desempleo = st.sidebar.slider("Tasa de Desempleo (%)", min_value=2.0, max_value=10.0, value=3.0, step=0.1)
bolsa_fase = st.sidebar.selectbox("Estado de la Bolsa (S&P 500 / BMV)", ["Cerca de Máximos Historicos", "Consolidación / Neutral", "Caída Severa / Mercado Bajista"])

# Algoritmo de Diagnóstico del Ciclo
def diagnosticar_ciclo(pib, inflacion, tasa, desempleo, bolsa):
    # Puntuaciones para clasificar la fase
    if pib > 2.5 and inflacion <= 4.0 and tasa <= 7.0 and desempleo < 3.5:
        fase = "EXPANSIÓN"
        descripcion = "La economía está creciendo con fuerza, las empresas venden más y el consumo es dinámico."
        color = "#2ecc71"
        portafolio = {"ETFs / Acciones": 55, "FIBRAS": 25, "Crowdfunding / Negocios": 15, "CETES / Renta Fija": 5}
    elif inflacion > 5.0 or (tasa >= 9.0 and pib > 0):
        fase = "PICO"
        descripcion = "La economía está al máximo de capacidad. Se presentan presiones inflacionarias y altas tasas de interés para frenar el sobrecalentamiento."
        color = "#e74c3c"
        portafolio = {"CETES / Renta Fija": 50, "FIBRAS": 25, "ETFs / Acciones (DCA)": 20, "Efectivo / Liquidez": 5}
    elif pib <= 0.5 and desempleo >= 3.5:
        fase = "RECESIÓN"
        descripcion = "La actividad económica se contrae, aumenta el desempleo y cae el consumo."
        color = "#e67e22"
        portafolio = {"CETES / Renta Fija L.P.": 60, "Efectivo / Liquidez": 25, "FIBRAS": 10, "ETFs / Acciones": 5}
    elif bolsa == "Caída Severa / Mercado Bajista" and tasa < 8.0 and inflacion <= 4.5:
        fase = "VALLE (Suelo)"
        descripcion = "Punto de máxima oportunidad. Miedo extremo en los mercados, valuaciones baratas y preparación para la recuperación."
        color = "#3498db"
        portafolio = {"ETFs / Acciones": 50, "FIBRAS": 25, "Crowdfunding Inmobiliario": 15, "CETES / Renta Fija": 10}
    else:
        fase = "DESACELERACIÓN / TRANSICIÓN"
        descripcion = "La economía se enfría, el PIB se desacelera pero la inflación y el desempleo se mantienen moderados."
        color = "#f1c40f"
        portafolio = {"CETES / Renta Fija": 45, "FIBRAS": 30, "ETFs / Acciones (DCA)": 20, "Efectivo / Liquidez": 5}
    
    return fase, descripcion, color, portafolio

fase, descripcion, color, portafolio = diagnosticar_ciclo(pib, inflacion, tasa_banxico, desempleo, bolsa_fase)

# Mostrar Diagnóstico
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(f"### Fase Actual Detectada:")
    st.markdown(f"<h1 style='color: {color};'>{fase}</h1>", unsafe_allow_html=True)
    st.info(descripcion)

with col2:
    st.markdown("### 📊 Asignación de Portafolio Recomendada")
    df_portafolio = pd.DataFrame(list(portafolio.items()), columns=['Activo', 'Porcentaje (%)'])
    
    fig = go.Figure(data=[go.Pie(labels=df_portafolio['Activo'], values=df_portafolio['Porcentaje (%)'], hole=.4)])
    fig.update_layout(margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("### 🗺️ Visualización del Ciclo Económico")

# Gráfica del ciclo
x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

fig_ciclo = go.Figure()
fig_ciclo.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Ciclo Económico', line=dict(color='gray', width=3)))

# Posición según la fase
posiciones = {
    "EXPANSIÓN": (np.pi/4, np.sin(np.pi/4)),
    "PICO": (np.pi/2, np.sin(np.pi/2)),
    "DESACELERACIÓN / TRANSICIÓN": (3*np.pi/4, np.sin(3*np.pi/4)),
    "RECESIÓN": (5*np.pi/4, np.sin(5*np.pi/4)),
    "VALLE (Suelo)": (3*np.pi/2, np.sin(3*np.pi/2))
}

px, py = posiciones.get(fase, (3*np.pi/4, np.sin(3*np.pi/4)))
fig_ciclo.add_trace(go.Scatter(x=[px], y=[py], mode='markers+text', name='Estás Aquí',
                               marker=dict(size=18, color=color),
                               text=[f"📍 Estás Aquí ({fase})"], textposition="top center"))

fig_ciclo.update_layout(
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    height=350,
    margin=dict(t=20, b=20, l=20, r=20)
)

st.plotly_chart(fig_ciclo, use_container_width=True)