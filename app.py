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
# CONFIGURACIÓN DE PÁGINA Y ESTILOS CUSTOM (Diseño Limpio y Seguro)
# ==============================================================================
st.set_page_config(page_title="Club Repiola - Eventos", layout="centered")

# CSS seguro para las tarjetas contenedoras de la lista principal
st.markdown("""
    <style>
    .event-card {
        background-color: #1A1A1A;
        border: 1px solid #333;
        border-left: 5px solid #E11D74;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 5px;
    }
    .card-title { color: #FFD31D !important; font-size: 22px !important; font-weight: bold !important; margin-bottom: 5px !important; font-family: sans-serif !important; }
    .card-date { color: #00A8CC !important; font-size: 16px !important; margin-bottom: 10px !important; font-family: sans-serif !important; }
    .badge-pago { background-color: #E11D74 !important; color: white !important; padding: 4px 8px !important; border-radius: 5px !important; font-size: 12px !important; font-weight: bold !important; display: inline-block !important; }
    .badge-gratis { background-color: #28a745 !important; color: white !important; padding: 4px 8px !important; border-radius: 5px !important; font-size: 12px !important; font-weight: bold !important; display: inline-block !important; }
    .badge-info { background-color: #6c757d !important; color: white !important; padding: 4px 8px !important; border-radius: 5px !important; font-size: 12px !important; font-weight: bold !important; display: inline-block !important; }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# BASE DE DATOS DE EVENTOS (Corregida con extensión .jpeg)
# ==============================================================================
EVENTOS = [
    {
        "id": "tiktu_01",
        "titulo": "Tiktuarawitaki en vivo: poesía, música e ilustración",
        "fecha": "Viernes 03 de Julio de 2026",
        "hora": "21:00 hrs",
        "imagen": "image_0563da.jpeg",  # <-- Cambiado a .jpeg
        "show_info": "🎟️ Entrada/Adhesión voluntaria en puerta desde $3.000",
        "descripcion": """Te invitamos a ser parte de una presentación especial de Tiktuarawitaki: Revitalizando la Herencia Cultural 🎨📖🎶

Una experiencia interdisciplinaria que une dibujo en vivo, poesía y música, inspirada en la obra de Gabriela Mistral y Manuel Rojas, donde la palabra, la imagen y el sonido se encuentran para dar vida a una nueva mirada sobre nuestra memoria cultural.

Esta presentación tiene además un propósito muy especial: reunir fondos para nuestra participación en una próxima presentación en Buenos Aires, llevando esta propuesta chilena a nuevos espacios de encuentro artístico y cultural. 🇨🇱✨""",
        "politicas": """
1. **Abono Consumible:** El valor para reservar tus asientos es de **$10.000**, los cuales se descuentan en su totalidad de lo que consumas en el local.
2. **Adhesión del Show:** El evento cuenta con una adhesión voluntaria en puerta sugerida desde **$3.000** destinada a los artists.
3. **Política de Cancelación:** Si avisas con un mínimo de **24 horas de anticipación**, se te devolverá el 100% del abono.
4. **Tolerancia de espera:** Tus asientos se guardarán **solo por 30 minutos** iniciado el evento (hasta las 21:30 hrs).
        """
    },
    {
        "id": "soa_01",
        "titulo": "Soa Borgoña en: Salida (De todo se sale) 🎭",
        "fecha": "Sábado 04 de Julio de 2026",
        "hora": "20:00 hrs",
        "imagen": "image_0563bc.jpeg",  # <-- Cambiado a .jpeg
        "show_info": "🎁 Entrada Liberada (Aporte Voluntario al artista)",
        "descripcion": "Disfruta de una íntima y potente velada junto a Soa Borgoña en su presentación interactiva. Música, reflexiones y arte se conjugan bajo la premisa de que 'De todo se sale'. Una propuesta imperdible para comenzar el sábado por la noche.",
        "politicas": """
1. **Abono Consumible:** El valor para reservar tus asientos es de **$10.000**, los cuales se descuentan en su totalidad de lo que consumas en el local.
2. **Entrada Liberada:** El show no cobra una entrada fija. Te invitamos a realizar un aporte voluntario al finalizar la presentación para apoyar al artista.
3. **Política de Cancelación:** Si avisas con un mínimo de **24 horas de anticipación**, se te devolverá el 100% del abono.
4. **Tolerancia de espera:** Tus asientos se guardarán **solo por 30 minutos** iniciado el evento (hasta las 20:30 hrs).
        """
    },
    {
        "id": "karaoke_01",
        "titulo": "Sábado de Karaoke 🎤",
        "fecha": "Sábado 04 de Julio de 2026",
        "hora": "22:00 hrs",
        "imagen": None,
        "show_info": "🎁 Entrada Liberada",
        "descripcion": "¡Saca el artista que llevas dentro! Una noche cargada de buena música y ruletas con premios justo después de la función de teatro. Ideal para celebrar con amigos en un ambiente ultra prendido.",
        "politicas": """
1. **Abono Consumible:** El valor para reservar tus asientos es de **$10.000**, los cuales se descuentan en su totalidad de lo que consumas en el local.
2. **Entrada Liberada:** No se cobra entrada por asistir al karaoke. Te invitamos a dejarle una propina voluntaria a la animadora para apoyar el formato en vivo.
3. **Política de Cancelación:** Si avisas con un mínimo de **24 horas de anticipación**, se te devolverá el 100% del abono.
4. **Tolerancia de espera:** Tus asientos se guardarán **solo por 30 minutos** (hasta las 22:30 hrs).
        """
    }
]

# ==============================================================================
# MANEJO DE ESTADO (Navegación y Asientos Disponibles)
# ==============================================================================
if "vista" not in st.session_state:
    st.session_state.vista = "lista"
if "evento_sel" not in st.session_state:
    st.session_state.evento_sel = None

# Inicializar disponibilidad de asientos para cada evento (Capacidad: 35 asientos)
if "asientos_disponibles" not in st.session_state:
    st.session_state.asientos_disponibles = {ev["id"]: 35 for ev in EVENTOS}

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
    st.markdown("### 🕒 Horario")
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
# VISTA 1: HOME - EXPLORADOR DE EVENTOS
# ==============================================================================
if st.session_state.vista == "lista":
    try:
        st.image("titulo_repiola.png", use_container_width=True)
    except:
        st.title("Club Repiola")

    st.subheader("Próximos Eventos")
    st.write("Explora nuestra cartelera y presiona el botón para reservar tus asientos.")
    st.write("---")

    st.warning("⚠️ **Nota sobre Reservas:** Todas las reservas requieren un abono de **$10.000**, el cual es **100% consumible** en el local.")
    st.info("Disponemos de solo 35 asientos por función para resguardar la comodidad y la intimidad del show.")
    st.write("")

    for ev in EVENTOS:
        badge_html = '<span class="badge-pago">Mesa Requiere Abono ($10.000)</span>'
        asientos_libres = st.session_state.asientos_disponibles[ev["id"]]

        html_tarjeta = f"""
        <div class="event-card">
            <div class="card-title">{ev['titulo']}</div>
            <div class="card-date">📅 {ev['fecha']} | ⏰ {ev['hora']}</div>
            {badge_html} 
            <br><span style="color:gray; font-size:13px;">Acceso Show: {ev['show_info']}</span>
            <br><span style="color:#00A8CC; font-size:14px; font-weight:bold;">🪑 Asientos Disponibles: {asientos_libres} / 35</span>
        </div>
        """
        st.markdown(html_tarjeta, unsafe_allow_html=True)
        
        texto_boton = "✨ Ver Información y Reservar Asientos"
        if st.button(texto_boton, key=ev['id'], use_container_width=True):
            ir_a_detalles(ev)
            st.rerun()
            
        st.write("")


# ==============================================================================
# VISTA 2: PÁGINA DE DETALLE Y FORMULARIO DE RESERVA
# ==============================================================================
elif st.session_state.vista == "detalle":
    ev = st.session_state.evento_sel
    asientos_libres = st.session_state.asientos_disponibles[ev["id"]]
    
    if st.button("⬅️ Volver a la lista de eventos"):
        volver_a_lista()
        st.rerun()

    st.write("")
    st.title(ev['titulo'])
    
    # 🛠️ RENDERIZAR IMAGEN OPTIMIZADA CON PATHLIB Y BUSCADOR AUTOMÁTICO
    if ev['imagen']:
        from pathlib import Path
        
        # Eliminamos la extensión para buscar el nombre base (ej: "image_0563da")
        nombre_base = Path(ev['imagen']).stem
        carpeta_actual = Path(__file__).parent
        
        # Buscamos cualquier archivo en la carpeta que empiece con ese nombre
        archivo_encontrado = None
        for archivo in carpeta_actual.glob(f"{nombre_base}.*"):
            if archivo.suffix.lower() in [".jpg", ".jpeg", ".png"]:
                archivo_encontrado = archivo
                break
        
        # Si lo encuentra, lo muestra. Si no, te dirá exactamente en pantalla dónde lo está buscando.
        if archivo_encontrado and archivo_encontrado.exists():
            st.image(str(archivo_encontrado), use_container_width=True)
        else:
            st.error(f"⚠️ Archivo no detectado en: {carpeta_actual.resolve()}/")
            st.caption(f"Asegúrate de que el afiche esté guardado en esa ruta exacta con el nombre: **{nombre_base}**")

    st.info(f"📅 **Fecha:** {ev['fecha']} | ⏰ **Hora:** {ev['hora']} | 🪑 **Cupos Restantes:** {asientos_libres} asientos libres.")
