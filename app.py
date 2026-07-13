# ==============================================================================
# PARCHE DE COMPATIBILIDAD PYTHON 3.13 + STREAMLIT
# ==============================================================================
import builtins
import importlib
import os
import sys
from datetime import datetime, date
import pandas as pd
import requests
import streamlit as st

if not hasattr(builtins, "sys"):
    builtins.sys = sys
if "sys" not in sys.modules:
    sys.modules["sys"] = sys

# ==============================================================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS CUSTOM
# ==============================================================================
st.set_page_config(page_title="Club Repiola - Eventos", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0F0F12; }
    .event-card-clean {
        background-color: #1A1A22;
        border: 1px solid #2A2A35;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: -10px;
    }
    .card-title-clean { 
        color: #FFFFFF !important; 
        font-size: 22px !important; 
        font-weight: 700 !important; 
        margin-bottom: 6px !important; 
    }
    .card-subtitle-clean { 
        color: #A0A0AB !important; 
        font-size: 15px !important; 
        margin-bottom: 14px !important; 
    }
    .badge-brand { 
        background-color: #E11D74; 
        color: white !important; 
        padding: 4px 10px; 
        border-radius: 6px; 
        font-size: 12px; 
        font-weight: 600; 
        display: inline-block;
        margin-right: 8px;
    }
    .badge-terraza { 
        background-color: #28a745; 
        color: white !important; 
        padding: 4px 10px; 
        border-radius: 6px; 
        font-size: 12px; 
        font-weight: 600; 
        display: inline-block;
    }
    .bank-box {
        background-color: #16161F;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #E11D74;
        margin: 20px 0;
    }
    .stButton>button {
        background-color: #E11D74 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #FF2E93 !important;
        transform: translateY(-1px);
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# BASE DE DATOS DE EVENTOS
# ==============================================================================
LISTA_EVENTOS_CRUDO = [
    {
        "id": "terraza_diaria",
        "titulo": "Reserva Espacio Terraza (Sin Show) 🌿",
        "dt_fecha": date(2026, 12, 31), # Fecha lejana para que siempre esté disponible
        "fecha": "Disponible Jueves a Sábado",
        "hora": "Desde las 18:00 hrs",
        "imagen": None, 
        "show_info": "Entrada Liberada",
        "descripcion": """¿Quieres venir a compartir sin necesariamente ver el show? 
        Nuestra terraza al aire libre es el lugar perfecto. 
        \n\n✅ Espacio para hasta 20 personas en total.
        \n✅ Ambiente relajado y al aire libre.
        \n❌ En este sector no hay visibilidad del show principal ni ruido fuerte de amplificación.""",
        "politicas": "* **Abono Consumible:** $10.000 para reservar la mesa (se descuenta al 100% de tu consumo).\n* **Capacidad:** Terraza habilitada para grupos de hasta 20 personas.\n* **Ubicación:** Espacio al aire libre."
    },
    {
        "id": "carlos_encina_10",
        "titulo": "Carlos Encina: Wenachoro 🎤",
        "dt_fecha": date(2026, 7, 10), # Ya pasó (10 de Julio), se filtrará automáticamente
        "fecha": "Viernes 10 de Julio de 2026",
        "hora": "21:30 hrs",
        "imagen": "image_09c622.jpg",
        "show_info": "Entrada Liberada (Aporte Voluntario)",
        "descripcion": """¡Vuelve el humor al Club! Carlos Encina presenta 'Tengo problemas con el frío - Wenachoro'. 
        Una rutina cargada de risas para pasar el invierno de la mejor manera.""",
        "politicas": "* **Abono Consumible:** $10.000 para reserva de mesa.\n* **Show:** Entrada liberada con aporte voluntario al artista al sobre."
    },
    {
        "id": "lecturas_clandestinas_24",
        "titulo": "Lecturas Clandestinas 🎭📖",
        "dt_fecha": date(2026, 7, 24),
        "fecha": "Viernes 24 de Julio de 2026",
        "hora": "20:00 hrs",
        "imagen": "image_465742.jpg",
        "show_info": "Entrada Liberada",
        "descripcion": """¡Una noche mágica de poesía, ilustración y encuentro cultural en el Bar Repiola! ✨ 

Ven a disfrutar de una íntima velada artística con la presentación de destacados creadores e ilustradores locales.

**Invitados Especiales:**
* Pavella Coppola
* Sergio Ojeda
* Fer Olivares Pereira
* Octavio Gallardo
* Seis
* César Millahueique

🎨 *Ilustración en vivo por Memy & Carnivale.*""",
        "politicas": """
* **Abono Consumible:** El valor para reservar tus asientos es de **$10.000**, los cuales se descuentan en su totalidad de lo que consumas en el local.
* **Entrada Liberada:** El evento cuenta con acceso liberado. Te sugerimos realizar un aporte voluntario para apoyar el trabajo de los artistas invitados.
* **Política de Cancelación:** Si avisas con un mínimo de **24 horas de anticipación**, se te devolverá el 100% del abono.
* **Tolerancia de espera:** Tus asientos se guardarán **solo por 30 minutos** iniciado el evento (hasta las 20:30 hrs).
        """
    },
    {
        "id": "espirocleta_31",
        "titulo": "EliasYuyo Espirocleta: Tú eliges los chistes 🎭",
        "dt_fecha": date(2026, 7, 31),
        "fecha": "Viernes 31 de Julio de 2026",
        "hora": "21:00 hrs",
        "imagen": "image_09c605.jpg",
        "show_info": "Entrada Liberada (Aporte Voluntario)",
        "descripcion": """Elias Yuyo presenta 'Espirocleta'. Un show interactivo de stand-up comedy donde el público tiene el absoluto control de los temas. 
        \n\n¡Chistes cortos, traumas, colegio, abuelos, corazón coreano y mucho más en una dinámica única!""",
        "politicas": "* **Abono Consumible:** El valor para reservar es de **$10.000**, descontables de tu consumo.\n* **Show:** Entrada liberada con aporte voluntario sugerido al finalizar la función."
    }
]

# --- LÓGICA DE FILTRADO AUTOMÁTICO ---
# Filtra y muestra solo los eventos cuya fecha sea igual o posterior al día de hoy.
hoy = date.today()
EVENTOS = [ev for ev in LISTA_EVENTOS_CRUDO if ev['dt_fecha'] >= hoy]

# ==============================================================================
# MANEJO DE ESTADO
# ==============================================================================
if "vista" not in st.session_state:
    st.session_state.vista = "lista"
if "evento_sel" not in st.session_state:
    st.session_state.evento_sel = None
if "reserva_exitosa" not in st.session_state:
    st.session_state.reserva_exitosa = False
if "info_reserva" not in st.session_state:
    st.session_state.info_reserva = {}

def ir_a_detalles(evento):
    st.session_state.evento_sel = evento
    st.session_state.vista = "detalle"
    st.session_state.reserva_exitosa = False

def volver_a_lista():
    st.session_state.vista = "lista"
    st.session_state.evento_sel = None
    st.session_state.reserva_exitosa = False
    st.session_state.info_reserva = {}

# ==============================================================================
# BARRA LATERAL
# ==============================================================================
with st.sidebar:
    try:
        st.image("logorepiola.jpg", use_container_width=True)
    except:
        st.subheader("Club Repiola")

    st.markdown("### 🕒 Horario")
    st.caption("**Jueves:** 18:00 a 24:00 hrs\n\n**Viernes y Sábado:** 18:00 a 03:00 hrs")
    st.markdown("---")
    st.markdown("### 📍 Ubicación")
    st.caption("Vicuña Rozas 5032, Quinta Normal, Santiago")
    st.markdown("---")
    st.link_button("💬 WhatsApp Ayuda", "https://wa.me/56996777779", use_container_width=True)

# ==============================================================================
# VISTA 1: CARTELERA
# ==============================================================================
if st.session_state.vista == "lista":
    try:
        st.image("titulo_repiola.png", use_container_width=True)
    except:
        st.title("Club Repiola")

    st.markdown("## Cartelera Próximos Eventos")
    st.markdown("Selecciona un evento de la cartelera para ver los detalles y reservar tus asientos.")
    st.markdown("> **Nota:** Las reservas de mesas requieren un abono de $10.000, el cual se descontará al 100% de tu consumo en el local.")
    st.write("")
    
    if not EVENTOS:
        st.info("No hay eventos programados por ahora. ¡Vuelve pronto!")
    
    for ev in EVENTOS:
        # Estilo diferente si es el espacio terraza
        badge_html = '<span class="badge-terraza">🌿 Aire Libre (Sin Show)</span>' if "terraza" in ev['id'] else '<span class="badge-brand">🎭 Show en Vivo</span>'
        
        html_tarjeta = f"""
        <div class="event-card-clean">
            <div class="card-title-clean">{ev['titulo']}</div>
            <div class="card-subtitle-clean">📅 {ev['fecha']} &nbsp;&middot;&nbsp; ⏰ {ev['hora']}</div>
            {badge_html}
            <div style="margin-top: 10px; font-size: 13px; color: #8E8E93;">Ubicación/Acceso: {ev['show_info']}</div>
        </div>
        """
        st.markdown(html_tarjeta, unsafe_allow_html=True)
        
        if st.button("Ver Información y Reservar", key=ev['id'], use_container_width=True):
            ir_a_detalles(ev)
            st.rerun()
        st.write("")

# ==============================================================================
# VISTA 2: DETALLE Y RESERVA
# ==============================================================================
elif st.session_state.vista == "detalle":
    ev = st.session_state.evento_sel
    
    if st.button("← Volver a la cartelera", key="btn_back"):
        volver_a_lista()
        st.rerun()

    st.write("")

    if st.session_state.reserva_exitosa:
        st.balloons()
        info = st.session_state.info_reserva
        st.success(f"🎉 ¡Pre-reserva de {info['asientos']} asientos registrada exitosamente!")
        
        st.markdown("""
            <div style="background-color: #16161F; padding: 20px; border-radius: 8px; border: 1px solid #E11D74; margin-bottom: 20px; text-align:center;">
                <span style="color: #E11D74; font-size: 18px; font-weight: bold;">⚠️ ¡ÚLTIMO PASO OBLIGATORIO!</span><br><br>
                <span style="font-size: 15px; color: #FFF;">Tus datos ya están guardados. Para validar definitivamente tus asientos, presiona el botón rosado de abajo para enviarnos el comprobante de transferencia directo a nuestro WhatsApp.</span>
            </div>
        """, unsafe_allow_html=True)
        
        mensaje_wa = (
            f"¡Hola! 🍹 Acabo de registrar una reserva desde la Ticketera Web.\n\n"
            f"👤 *Nombre:* {info['nombre']}\n"
            f"🆔 *RUT:* {info['rut']}\n"
            f"📅 *Evento:* {ev['titulo']}\n"
            f"🪑 *Asientos:* {info['asientos']}\n\n"
            f"Acepto los términos de abono. Adjunto el comprobante de transferencia por $10.000 para validar."
        )
        url_whatsapp = f"https://wa.me/56996777779?text={requests.utils.quote(mensaje_wa)}"
        
        st.link_button("🟢 Enviar Comprobante por WhatsApp", url_whatsapp, type="primary", use_container_width=True)
        st.write("")
        
        if st.button("Volver al Inicio", use_container_width=True):
            volver_a_lista()
            st.rerun()
    else:
        st.markdown(f"# {ev['titulo']}")
        if ev['imagen']:
            try:
                st.image(ev['imagen'], use_container_width=True)
            except:
                pass

        st.markdown(f"**📅 Fecha:** {ev['fecha']} | **⏰ Hora:** {ev['hora']}")
        st.write("---")
        
        st.markdown("### Sobre este evento")
        st.markdown(ev['descripcion'])
        
        # Datos bancarios para transferencia
        st.markdown(f"""
        <div class="bank-box">
            <h4 style="color: #FFFFFF; margin-top:0; font-weight:600;">Datos de Transferencia para Reservar</h4>
            <p style="color: #A0A0AB; font-size: 14px; margin-bottom: 12px;">Para asegurar tus asientos, transfiere el abono (100% consumible en el local) a la siguiente cuenta:</p>
            <table style="width:100%; border-collapse: collapse; font-size: 14px; color: #FFF;">
                <tr><td style="padding: 4px 0; color: #8E8E93;">Nombre del Titular:</td><td><b>Juan Carlos Quiroz</b></td></tr>
                <tr><td style="padding: 4px 0; color: #8E8E93;">Banco:</td><td><b>Santander (Cuenta Corriente)</b></td></tr>
                <tr><td style="padding: 4px 0; color: #8E8E93;">Rut:</td><td><b>11.633.847-5</b></td></tr>
                <tr><td style="padding: 4px 0; color: #8E8E93;">N de Cuenta:</td><td><b>0000-64583867</b></td></tr>
                <tr><td style="padding: 4px 0; color: #8E8E9
