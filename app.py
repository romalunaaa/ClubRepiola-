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
# CONFIGURACIÓN DE PÁGINA
# ==============================================================================
st.set_page_config(page_title="Club Repiola - Eventos", layout="centered")

# Custom CSS para que las tarjetas se vean geniales
st.markdown("""
    <style>
    .event-card {
        background-color: #1A1A1A;
        border: 1px solid #333;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 5px solid #E11D74;
    }
    .event-title { color: #FFD31D; font-size: 22px; font-weight: bold; margin-bottom: 5px; }
    .event-date { color: #00A8CC; font-size: 16px; margin-bottom: 10px; }
    .badge-pago { background-color: #E11D74; color: white; padding: 2px 8px; border-radius: 5px; font-size: 12px; }
    .badge-gratis { background-color: #28a745; color: white; padding: 2px 8px; border-radius: 5px; font-size: 12px; }
    .badge-info { background-color: #6c757d; color: white; padding: 2px 8px; border-radius: 5px; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# BASE DE DATOS DE EVENTOS (Actualizada con las nuevas políticas de abono)
# ==============================================================================
# Tipos: 'reserva_gratis', 'reserva_pago', 'solo_info'
EVENTOS = [
    {
        "id": "karaoke_01",
        "titulo": "Sábado de Karaoke 🎤",
        "fecha": "Todos los Sábados",
        "hora": "22:00 hrs",
        "tipo": "reserva_gratis",
        "descripcion": "¡Saca el artista que llevas dentro! Una noche cargada de buena música y ruletas con premios. Ideal para celebrar cumpleaños.",
        "politicas": """
            <li><b>Entrada Liberada:</b> No se cobra abono previo para este evento.</li>
            <li><b>Tolerancia de espera:</b> La mesa se reserva <b>solo por 30 minutos</b> desde el inicio del evento (22:30 hrs). Pasado ese tiempo, la mesa quedará libre para el público general.</li>
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
        "descripcion": "Experiencia interdisciplinaria de dibujo en vivo, poesía y música. Fondos para gira en Buenos Aires.",
        "datos_pago": {
            "banco": "BancoEstado (CuentaRUT)",
            "cuenta": "11.633.847-5",
            "monto": "$10.000 (Abono reembolsable/consumible)",
            "correo": "clubrepiola@gmail.com"
        },
        "politicas": """
            <li><b>Abono Consumible:</b> El valor de la reserva es de <b>$10.000</b>, los cuales se descontarán en su totalidad de tu consumo total en el local.</li>
            <li><b>Política de Cancelación:</b> Si avisas con un mínimo de <b>24 horas de anticipación</b>, se te devolverá el 100% del dinero. Si avisas tarde o no avisas, <b>no habrá devolución</b>.</li>
            <li><b>Tolerancia de espera:</b> La mesa se guardará <b>solo por 30 minutos</b> iniciado el evento. Pasado ese tiempo, la mesa se liberará para las personas que vayan llegando.</li>
        """,
        "precio_min": "$10.000"
    },
    {
        "id": "promo_jueves",
        "titulo": "Jueves de Promo: 2x1 🍹",
        "fecha": "Todos los Jueves",
        "hora": "18:00 a 24:00 hrs",
        "tipo": "solo_info",
        "descripcion": "Todos los Jueves tenemos 2x1 en combinados nacionales. ¡No requiere reserva, solo llega temprano!",
        "politicas": "<li>Promoción válida hasta agotar stock. No acumulable. Ingreso por orden de llegada.</li>",
        "precio_min": "Solo Info"
    }
]
# ==============================================================================
# MANEJO DE ESTADO (Navegación)
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
# SIDEBAR (Común para ambas vistas)
# ==============================================================================
with st.sidebar:
    try:
        st.image("logorepiola.jpg", use_container_width=True)
    except:
        st.header("Club Repiola")
    
    st.markdown("---")
    st.markdown("### 🕒 Horario Otoño")
    st.write("• **Jueves:** 18:00 a 00:00\n• **Viernes/Sábado:** 18:00 a 03:00")
    st.markdown("---")
    st.markdown("### 📍 Ubicación")
    st.caption("Vicuña Rozas 5032, Quinta Normal")
    st.markdown("---")
    st.success("[💬 WhatsApp Ayuda](https://wa.me/56996777779)")

# ==============================================================================
# VISTA 1: LISTA DE EVENTOS
# ==============================================================================
if st.session_state.vista == "lista":
    try:
        st.image("titulo_repiola.png", use_container_width=True)
    except:
        st.title("Club Repiola")

    st.subheader("Próximos Eventos")
    st.write("Haz clic en un evento para ver detalles y reservar.")

    for ev in EVENTOS:
        # Definir etiqueta según tipo
        if ev['tipo'] == "reserva_gratis":
            badge = '<span class="badge-gratis">Reserva Gratis</span>'
        elif ev['tipo'] == "reserva_pago":
            badge = '<span class="badge-pago">Requiere Adhesión</span>'
        else:
            badge = '<span class="badge-info">Sólo Información</span>'

        # Render de la tarjeta HTML
        st.markdown(f"""
            <div class="event-card">
                <div class="event-title">{ev['titulo']}</div>
                <div class="event-date">📅 {ev['fecha']} | ⏰ {ev['hora']}</div>
                {badge} <span style="color:gray; font-size:12px;">Min: {ev['precio_min']}</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Botón de Streamlit para acción
        texto_boton = "Ver Información y Reservar" if ev['tipo'] != "solo_info" else "Ver Más Información"
        if st.button(texto_boton, key=ev['id'], use_container_width=True):
            ir_a_detalles(ev)
            st.rerun()

# ==============================================================================
# VISTA 2: DETALLE DEL EVENTO Y FORMULARIO
# ==============================================================================
elif st.session_state.vista == "detalle":
    ev = st.session_state.evento_sel
    
    if st.button("⬅️ Volver a todos los eventos"):
        volver_a_lista()
        st.rerun()

    st.title(ev['titulo'])
    st.info(f"📅 **Fecha:** {ev['fecha']} | ⏰ **Hora:** {ev['hora']}")
    
    st.markdown(f"### Sobre el evento")
    st.write(ev['descripcion'])

    # Si el evento es de pago, mostrar tarjeta de transferencia
    if ev['tipo'] == "reserva_pago":
        pago = ev['datos_pago']
        html_pago = f"""
        <div style="background-color: #1A1A1A; padding: 20px; border-radius: 12px; border: 2px solid #E11D74;">
            <h4 style="color: #FFD31D; margin-top:0;">Datos de Transferencia</h4>
            <ul style="color: #00A8CC;">
                <li><b>Banco:</b> {pago['banco']}</li>
                <li><b>Cuenta:</b> {pago['cuenta']}</li>
                <li><b>Monto:</b> {pago['monto']}</li>
                <li><b>Correo:</b> {pago['correo']}</li>
            </ul>
            <p style="font-size:12px; color:white;">⚠️ <i>{ev['politicas']}</i></p>
        </div>
        """
        st.markdown(html_pago, unsafe_allow_html=True)
    
    elif ev['tipo'] == "reserva_gratis":
        st.success(f"✅ **Entrada Liberada:** {ev['politicas']}")

    # Formulario (Solo si permite reserva)
    if ev['tipo'] in ["reserva_gratis", "reserva_pago"]:
        st.write("---")
        with st.form("form_reserva"):
            st.subheader("Reserva tu lugar")
            mesa = st.selectbox("Mesa para:", ["Mesa 1-2 pers", "Mesa 3-4 pers", "Terraza (Fumadores)"])
            nombre = st.text_input("Nombre Completo")
            rut = st.text_input("RUT (Para validar)")
            
            submit = st.form_submit_button("🚀 Confirmar Intención de Reserva")
            
            if submit:
                if nombre and rut:
                    # Lógica de Google Forms (Reutilizada de tu código original)
                    url_forms = "https://docs.google.com/forms/d/e/1FAIpQLSdv66lUkibd-_FgYIajnZAw6CvBnIvsfjkL_xpeWRBluWWNyQ/formResponse"
                    payload = {
                        "entry.2041447904": ev['titulo'],
                        "entry.44496726": mesa,
                        "entry.970850673": nombre,
                        "entry.2047753483": rut
                    }
                    try:
                        requests.post(url_forms, data=payload)
                        st.balloons()
                        
                        # Preparar WhatsApp
                        txt_wa = f"¡Hola! Reservé para *{ev['titulo']}*.\n👤 Nombre: {nombre}\n🆔 RUT: {rut}\n🪑 Mesa: {mesa}"
                        if ev['tipo'] == "reserva_pago":
                            txt_wa += "\n👇 Aquí adjunto mi comprobante."
                        
                        url_wa = f"https://wa.me/56996777779?text={requests.utils.quote(txt_wa)}"
                        
                        st.success("¡Datos enviados!")
                        st.link_button("🟢 Finalizar en WhatsApp", url_wa, type="primary", use_container_width=True)
                    except:
                        st.error("Error al conectar con el servidor.")
                else:
                    st.warning("Completa los campos obligatorios.")
    else:
        # Vista para eventos 'solo_info'
        st.warning("📍 Este evento no requiere reserva previa. ¡Te esperamos por orden de llegada!")
        st.markdown(f"**Condiciones:** {ev['politicas']}")
