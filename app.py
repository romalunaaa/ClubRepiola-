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
    
    # Renderizar Imagen del Evento de forma limpia (Si falla o no está, pasa en silencio)
    if ev['imagen']:
        try:
            st.image(ev['imagen'], use_container_width=True)
        except:
            pass

    st.info(f"📅 **Fecha:** {ev['fecha']} | ⏰ **Hora:** {ev['hora']} | 🪑 **Cupos Restantes:** {asientos_libres} asientos libres.")
    
    st.markdown("### Sobre este evento")
    st.markdown(ev['descripcion'])
    st.write("")

    # Cuadro Único de Instrucciones de Abono
    html_pago = (
        '<div style="background-color: #1A1A1A; padding: 20px; border-radius: 12px; border: 2px solid #E11D74;">'
        '<h4 style="color: #FFD31D; margin-top:0; font-family: sans-serif;">Instrucciones de Abono para la Mesa (CuentaRUT):</h4>'
        '<p style="color: #FFFFFF; margin-bottom: 10px;">Para asegurar tus asientos se requiere transferir un abono (100% consumible en el local):</p>'
        '<ul style="color: #00A8CC; padding-left: 20px;">'
        '<li><b>Banco:</b> BancoEstado (CuentaRUT)</li>'
        '<li><b>Número de Cuenta:</b> 11.633.847-5</li>'
        '<li><b>Monto del Abono:</b> $10.000</li>'
        '<li><b>Correo:</b> clubrepiola@gmail.com</li>'
        f'<li><b>Detalle del Show:</b> {ev["show_info"]}</li>'
        '</ul>'
        '</div>'
    )
    st.markdown(html_pago, unsafe_allow_html=True)
        
    st.write("")
    st.markdown("### ⚠️ Detalles del Evento (Términos y Condiciones):")
    st.markdown(ev['politicas'])
    st.write("")

    # FORMULARIO DE RESERVAS
    if asientos_libres > 0:
        with st.form("formulario_reserva_dinamico"):
            st.subheader("Completa tus datos para reservar")
            st.error("💳 **Este evento requiere Abono Consumible ($10.000) para asegurar los asientos.**")
            
            # Selector de cantidad de asientos (Mesa de 1 a 20 personas)
            max_seleccionable = min(20, asientos_libres)
            asientos_solicitados = st.selectbox(
                "¿Cuántos asientos necesitas para tu grupo?",
                list(range(1, max_seleccionable + 1)),
                format_func=lambda x: f"Mesa / Espacio para {x} persona{'s' if x > 1 else ''}"
            )

            nombre = st.text_input("Nombre Completo de quien asiste")
            rut = st.text_input("RUT del Titular (Para validar asistencia)")

            boton_confirmar = st.form_submit_button("🚀 Enviar y Reservar Espacio")

        if boton_confirmar:
            if nombre and rut:
                try:
                    url_formulario = "https://docs.google.com/forms/d/e/1FAIpQLSdv66lUkibd-_FgYIajnZAw6CvBnIvsfjkL_xpeWRBluWWNyQ/formResponse"
                    datos_reserva_forms = {
                        "entry.2041447904": ev['titulo'],
                        "entry.44496726": f"{asientos_solicitados} Asientos",
                        "entry.970850673": nombre,
                        "entry.2047753483": rut,
                    }

                    respuesta = requests.post(url_formulario, data=datos_reserva_forms)

                    if respuesta.status_code == 200:
                        # DESCONTAR DE LA DISPONIBILIDAD REAL
                        st.session_state.asientos_disponibles[ev["id"]] -= asientos_solicitados
                        
                        datos_nueva_reserva = {
                            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "Evento": ev['titulo'],
                            "Mesa": f"{asientos_solicitados} Asientos",
                            "Nombre": nombre,
                            "RUT": rut,
                            "Estado": "Pendiente",
                        }
                        nueva_reserva_df = pd.DataFrame([datos_nueva_reserva])
                        nueva_reserva_df.to_csv(
                            "reservas_local.csv",
                            mode="a",
                            header=not os.path.exists("reservas_local.csv"),
                            index=False,
                        )

                        st.balloons()
                        st.success(f"🎉 ¡Pre-reserva de {asientos_solicitados} asientos registrada con éxito!")

                        remate_wa = f"Acepto los términos de abono consumible. Adjunto comprobante de transferencia por $10.000 para validar mis asientos. 👇"
                        texto_instruccion_wa = "Para validar tus asientos, presiona el botón de abajo para abrir WhatsApp y <b>enviarnos la captura del comprobante de transferencia</b>."

                        mensaje_wa = (
                            f"¡Hola! 🍹 Acabo de registrar una reserva desde la Ticketera Web.\n\n"
                            f"👤 *Nombre:* {nombre}\n"
                            f"🆔 *RUT:* {rut}\n"
                            f"📅 *Evento:* {ev['titulo']}\n"
                            f"🪑 *Asientos Reservados:* {asientos_solicitados}\n\n"
                            f"{remate_wa}"
                        )

                        mensaje_codificado = requests.utils.quote(mensaje_wa)
                        url_whatsapp = f"https://wa.me/56996777779?text={mensaje_codificado}"

                        html_aviso_final = (
                            '<div style="background-color: #ff007f1a; padding: 15px; border-radius: 8px; border: 1px dashed #ff007f; margin-bottom: 15px;">'
                            '<p style="margin: 0; color: #ff007f; font-weight: bold; text-align: center;">⚠️ ¡ÚLTIMO PASO OBLIGATORIO! ⚠️</p>'
                            f'<p style="margin: 5px 0 0 0; font-size: 14px; text-align: center;">{texto_instruccion_wa}</p>'
                            '</div>'
                        )
                        st.markdown(html_aviso_final, unsafe_allow_html=True)
                        st.link_button("🟢 Notificar Reserva por WhatsApp", url_whatsapp, type="primary", use_container_width=True)
                        
                        st.button("Actualizar pantalla", on_click=volver_a_lista)
                        
                    else:
                        st.error(f"Error de comunicación con el servidor (Código {respuesta.status_code}).")
                except Exception as e:
                    st.error(f"Error al procesar la reserva: {e}")
            else:
                st.warning("Por favor, rellena tu Nombre y tu RUT antes de enviar la solicitud.")
    else:
        st.error("🚨 Lo sentimos, las reservas para este evento están AGOTADAS.")
