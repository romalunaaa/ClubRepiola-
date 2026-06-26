# ==============================================================================
# PARCHE DE COMPATIBILIDAD PYTHON 3.13 + STREAMLIT
# ==============================================================================
import builtins
import importlib
import os
import sys
from datetime import datetime
import pandas as pd
import requests
import streamlit as st

if not hasattr(builtins, "sys"):
    builtins.sys = sys
if "sys" not in sys.modules:
    sys.modules["sys"] = sys

# ==============================================================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS CUSTOM (Tarjetas como Botones)
# ==============================================================================
st.set_page_config(page_title="Club Repiola - Eventos", layout="centered")

# CSS personalizado para que toda la tarjeta actúe como botón interactivo
st.markdown("""
    <style>
    /* Estilizar el botón nativo de Streamlit para transformarlo en tarjeta */
    div.stButton > button {
        background-color: #1A1A1A !important;
        border: 1px solid #333 !important;
        border-left: 5px solid #E11D74 !important;
        border-radius: 15px !important;
        padding: 20px !important;
        width: 100% !important;
        text-align: left !important;
        margin-bottom: 15px !important;
        transition: transform 0.2s, border-color 0.2s !important;
    }
    /* Efecto Hover al pasar el mouse */
    div.stButton > button:hover {
        border-color: #E11D74 !important;
        transform: scale(1.01);
        background-color: #222222 !important;
    }
    /* Estilos de los textos internos de la tarjeta */
    .card-title { color: #FFD31D; font-size: 22px; font-weight: bold; margin-bottom: 5px; font-family: sans-serif; }
    .card-date { color: #00A8CC; font-size: 16px; margin-bottom: 10px; font-family: sans-serif; }
    .badge-pago { background-color: #E11D74; color: white; padding: 4px 8px; border-radius: 5px; font-size: 12px; font-weight: bold; }
    .badge-gratis { background-color: #28a745; color: white; padding: 4px 8px; border-radius: 5px; font-size: 12px; font-weight: bold; }
    .badge-info { background-color: #6c757d; color: white; padding: 4px 8px; border-radius: 5px; font-size: 12px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# BASE DE DATOS DE EVENTOS (Modificable)
# ==============================================================================
# Tipos soportados: 'reserva_gratis', 'reserva_pago', 'solo_info'
EVENTOS = [
    {
        "id": "karaoke_01",
        "titulo": "Sábado de Karaoke 🎤",
        "fecha": "Todos los Sábados",
        "hora": "22:00 hrs",
        "tipo": "reserva_gratis",
        "descripcion": "¡Saca el artista que llevas dentro! Una noche cargada de buena música y ruletas con premios. Ideal para celebrar cumpleaños en un ambiente ultra prendido.",
        "politicas": """
            <li><b>Entrada Liberada:</b> No se cobra abono previo para este evento.</li>
            <li><b>Tolerancia de espera:</b> La mesa se reserva <b>solo por 30 minutos</b> desde el inicio del evento (hasta las 22:30 hrs). Pasado ese tiempo, la mesa quedará libre para el público general.</li>
            <li><b>Propina:</b> Te invitamos a dejarle una propina voluntaria a la animadora para apoyar el karaoke en vivo.</li>
        """,
        "precio_min": "$0"
    },
    {
        "id": "tiktu_01",
        "titulo": "Tiktuarawitaki en Vivo 🎶",
        "fecha": "Viernes 03 de Julio",
        "hora": "21:00 hrs",
        "tipo": "reserva_pago",
        "descripcion": "Experiencia interdisciplinaria de dibujo en vivo, poesía y música inspirada en Gabriela Mistral y Manuel Rojas. Fondos para próxima gira en Buenos Aires.",
        "datos_pago": {
            "banco": "BancoEstado (CuentaRUT)",
            "cuenta": "11.633.847-5",
            "monto": "$10.000 (Abono transferido)",
            "correo": "clubrepiola@gmail.com"
        },
        "politicas": """
            <li><b>Abono Consumible:</b> El valor de la reserva es de <b>$10.000</b>, los cuales se descontarán en su totalidad de tu consumo total en el local.</li>
            <li><b>Política de Cancelación:</b> Si avisas con un mínimo de <b>24 horas de anticipación</b>, se te devolverá el 100% del dinero. Si avisas tarde o no avisas, <b>no habrá devolución</b>.</li>
            <li><b>Tolerancia de espera:</b> La mesa se guardará <b>solo por 30 minutos</b> iniciado el evento (hasta las 21:30 hrs). Pasado ese tiempo, la mesa se liberará para el público general.</li>
        """,
        "precio_min": "$10.000"
    },
    {
        "id": "promo_jueves",
        "titulo": "Jueves de Poesía",
        "fecha": "Todos los Jueves",
        "hora": "18:00 a 24:00 hrs",
        "tipo": "solo_info",
        "descripcion": "Todos los Jueves Poesía Clandestina. ¡Trae a tus amigos y disfruta de la poesía!",
        "politicas": "<li>Ingreso por orden de llegada.</li>",
        "precio_min": "Solo Info"
    }
]

# ==============================================================================
# MANEJO DE ESTADO DE NAVEGACIÓN
# ==============================================================================
if "vista" not in st.session_state:
    st.session_state.vista = "lista"
if "evento_sel" not in st.session_state:
    st.session_state.evento_sel = None

def ir_a_detalles(evento):
    st.session_state.evento_sel = evento
    st.session_state.vista = "detalle"

def volver_a_lista():
    st.session_state.vista = "lista"
    st.session_state.evento_sel = None

# ==============================================================================
# BARRA LATERAL (INFORMACIÓN DE LA PYME)
# ==============================================================================
with st.sidebar:
    try:
        st.image("logorepiola.jpg", use_container_width=True)
    except:
        st.subheader("Club Repiola")

    st.markdown("---")
    st.markdown("### 🕒 Horario Otoño")
    st.write("• **Jueves:** 18:00 a 24:00 hrs")
    st.write("• **Viernes y Sábado:** 18:00 a 03:00 hrs")
    st.write("• **Domingo:** Solo Eventos reservados.")

    st.markdown("---")
    st.markdown("### 📍 Ubicación")
    st.caption("Vicuña Rozas 5032, Quinta Normal, Santiago, Chile")

    st.markdown("---")
    st.markdown("### 📞 WhatsApp")
    st.success("[+56 9 9677 7779](https://wa.me/56996777779)")

# ==============================================================================
# VISTA 1: HOME - EXPLORADOR DE EVENTOS (PÁGINA TIPO TICKETERA)
# ==============================================================================
if st.session_state.vista == "lista":
    try:
        st.image("titulo_repiola.png", use_container_width=True)
    except:
        st.title("Club Repiola")

    st.subheader("Próximos Eventos")
    st.write("Selecciona el evento que te interesa para ver detalles y reservar.")
    st.write("---")

    # Alertas globales de la App
    st.warning("Cupos Limitados. Los fines de semana las mesas se llenan rápido.")
    st.info("**¡Hola! Te contamos:** Para aprovechar al máximo nuestro espacio, algunas de nuestras mesas se comparten con otros clientes. Tenlo en consideración al hacer tu reserva.")
    st.write("")

    # Renderizado iterativo de las tarjetas-botones
    for ev in EVENTOS:
        if ev['tipo'] == "reserva_gratis":
            badge_html = '<span class="badge-gratis">Reserva Gratis</span>'
        elif ev['tipo'] == "reserva_pago":
            badge_html = '<span class="badge-pago">Requiere Adhesión</span>'
        else:
            badge_html = '<span class="badge-info">Sólo Información</span>'

        # Estructura del contenido visual de la tarjeta
        html_tarjeta = f"""
            <div class="card-title">{ev['titulo']}</div>
            <div class="card-date">📅 {ev['fecha']} | ⏰ {ev['hora']}</div>
            {badge_html} <span style="color:gray; font-size:12px; margin-left:10px;">Valor: {ev['precio_min']}</span>
        """
        
        # Al presionar la tarjeta completa, se gatilla la redirección
        if st.button(html_tarjeta, key=ev['id']):
            ir_a_detalles(ev)
            st.rerun()

# ==============================================================================
# VISTA 2: PÁGINA DE DETALLE Y FORMULARIO DE RESERVA
# ==============================================================================
elif st.session_state.vista == "detalle":
    ev = st.session_state.evento_sel
    
    if st.button("VOLVER A LA LISTA DE EVENTOS"):
        volver_a_lista()
        st.rerun()

    st.write("")
    st.title(ev['titulo'])
    st.info(f"📅 **Fecha:** {ev['fecha']} | ⏰ **Hora:**
