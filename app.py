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

# CSS seguro para las tarjetas contenedoras (Markdown)
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
# BASE DE DATOS DE EVENTOS
# ==============================================================================
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
        "titulo": "Jueves de Promo: 2x1 🍹",
        "fecha": "Todos los Jueves",
        "hora": "18:00 a 24:00 hrs",
        "tipo": "solo_info",
        "descripcion": "Todos los Jueves tenemos 2x1 en combinados nacionales. ¡Trae a tus amigos y disfruta de la mejor previa de la semana!",
        "politicas": "<li>Promoción válida hasta agotar stock. No acumulable con otras promociones. Ingreso por orden de llegada.</li>",
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
# VISTA 1: HOME - EXPLORADOR DE EVENTOS
# ==============================================================================
if st.session_state.vista == "lista":
    try:
        st.image("titulo_repiola.png", use_container_width=True)
    except:
        st.title("Club Repiola")

    st.subheader("Próximos Eventos")
    st.write("Explora nuestra cartelera y presiona el botón para reservar tu mesa.")
    st.write("---")

    # Alertas globales
    st.warning("Cupos Limitados. Los fines de semana las mesas se llenan rápido.")
    st.info("**¡Hola! Te contamos:** Para aprovechar al máximo nuestro espacio, algunas de nuestras mesas se comparten con otros clientes. Tenlo en consideración al hacer tu reserva.")
    st.write("")

    # Renderizado seguro: Tarjeta HTML + Botón de Streamlit abajo
    for ev in EVENTOS:
        if ev['tipo'] == "reserva_gratis":
            badge_html = '<span class="badge-gratis">Reserva Gratis</span>'
        elif ev['tipo'] == "reserva_pago":
            badge_html = '<span class="badge-pago">Requiere Adhesión</span>'
        else:
            badge_html = '<span class="badge-info">Sólo Información</span>'

        # Dibujamos la tarjeta visual de forma segura usando markdown
        html_tarjeta = f"""
        <div class="event-card">
            <div class="card-title">{ev['titulo']}</div>
            <div class="card-date">📅 {ev['fecha']} | ⏰ {ev['hora']}</div>
            {badge_html} <span style="color:gray; font-size:12px; margin-left:10px;">Valor: {ev['precio_min']}</span>
        </div>
        """
        st.markdown(html_tarjeta, unsafe_allow_html=True)
        
        # Botón nativo de Streamlit justo debajo de la tarjeta para avanzar
        texto_boton = "✨ Ver Información y Reservar Mesa" if ev['tipo'] != "solo_info" else "👀 Ver Más Información"
        if st.button(texto_boton, key=ev['id'], use_container_width=True):
            ir_a_detalles(ev)
            st.rerun()
            
        st.write("") # Espacio de separación

# ==============================================================================
# VISTA 2: PÁGINA DE DETALLE Y FORMULARIO DE RESERVA
# ==============================================================================
elif st.session_state.vista == "detalle":
    ev = st.session_state.evento_sel
    
    if st.button("⬅️ Volver a la lista de eventos"):
        volver_a_lista()
        st.rerun()

    st.write("")
    st.title(ev['titulo'])
    st.info(f"📅 **Fecha:** {ev['fecha']} | ⏰ **Hora:** {ev['hora']}")
    
    st.markdown("### Sobre este evento")
    st.markdown(f"*{ev['descripcion']}*")
    st.write("")

    # DISEÑO DE TARJETAS INTERNAS CON RESTRICCIONES Y POLÍTICAS PROCESADAS
    if ev['tipo'] == "reserva_pago":
        pago = ev['datos_pago']
        html_pago = f"""
        <div style="background-color: #1A1A1A; padding: 20px; border-radius: 12px; border: 2px solid #E11D74; box-shadow: 0px 4px 15px rgba(225, 29, 116, 0.2);">
            <h4 style="color: #FFD31D; margin-top:0; font-family: sans-serif; letter-spacing: 1px;">Instrucciones de Reserva (CuentaRUT):</h4>
            <p style="margin-bottom: 15px; color: #FFFFFF;">Realiza la transferencia para congelar tu espacio de forma inmediata con toda la onda:</p>
            <ul style="color: #00A8CC; list-style-type: square; padding-left:20px;">
                <li><b>Banco:</b> {pago['banco']}</li>
                <li><b>Número de Cuenta:</b> {pago['cuenta']}</li>
                <li><b>Monto del Abono:</b> {pago['monto']}</li>
                <li><b>Correo:</b> {pago['correo']}</li>
            </ul>
            <h4 style="color: #ff007f; margin-top:15px; margin-bottom:5px;">⚠️ Detalles del Evento (Términos y Condiciones):</h4>
            <ol style="font-size: 14px; color: #FFFFFF; padding-left: 20px;">
                {ev['politicas']}
            </ol>
        </div>
        """
        st.markdown(html_pago, unsafe_allow_html=True)
    
    elif ev['tipo'] == "reserva_gratis":
        html_gratis = f"""
        <div style="background-color: #162A16; padding: 20px; border-radius: 12px; border: 2px solid #28a745; box-shadow: 0px 4px 15px rgba(40, 167, 69, 0.2);">
            <h4 style="color: #28a745; margin-top:0; font-family: sans-serif; letter-spacing: 1px;">✅ Información de Acceso (Entrada Liberada):</h4>
            <p style="margin-bottom: 15px; color: #FFFFFF;">Para este evento no necesitas realizar abonos previos de dinero:</p>
            <ul style="color: #00A8CC; list-style-type: square; padding-left:20px;">
                <li><b>Costo de Reserva:</b> Gratis / $0</li>
                <li><b>Acceso:</b> Solo debes asegurar tu cupo completando el formulario de abajo.</li>
            </ul>
            <h4 style="color: #28a745; margin-top:15px; margin-bottom:5px;">⚠️ Detalles del Evento (Términos y Condiciones):</h4>
            <ol style="font-size: 14px; color: #FFFFFF; padding-left: 20px;">
                {ev['politicas']}
            </ol>
        </div>
        """
        st.markdown(html_gratis, unsafe_allow_html=True)

    st.write("")

    # FORMULARIO DE ASIGNACIÓN
    if ev['tipo'] in ["reserva_gratis", "reserva_pago"]:
        with st.form("formulario_reserva_dinamico"):
            st.subheader("Completa tus datos para la mesa")
            
            if ev['tipo'] == "reserva_gratis":
                st.success("✅ **Este evento es de Entrada Liberada ($0).**")
            else:
                st.error("💳 **Este evento requiere Abono Reembolsable ($10.000).**")

            mesa_seleccionada = st.selectbox(
                "Selecciona tu Mesa preferida",
                ["Mesa para 1", "Mesa para 2", "Mesa para 3", "Mesa para 4", "Terraza"],
            )

            nombre = st.text_input("Nombre Completo de quien asiste")
            rut = st.text_input("RUT del Titular (Para validar transferencia/asistencia)")

            boton_confirmar = st.form_submit_button("🚀 Enviar y Reservar Espacio")

        if boton_confirmar:
            if nombre and rut:
                try:
                    url_formulario = "https://docs.google.com/forms/d/e/1FAIpQLSdv66lUkibd-_FgYIajnZAw6CvBnIvsfjkL_xpeWRBluWWNyQ/formResponse"
                    datos_reserva_forms = {
                        "entry.2041447904": ev['titulo'],
                        "entry.44496726": mesa_seleccionada,
                        "entry.970850673": nombre,
                        "entry.2047753483": rut,
                    }

                    respuesta = requests.post(url_formulario, data=datos_reserva_forms)

                    if respuesta.status_code == 200:
                        datos_nueva_reserva = {
                            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "Evento": ev['titulo'],
                            "Mesa": mesa_seleccionada,
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
                        st.success("🎉 ¡Pre-reserva registrada con éxito!")

                        if ev['tipo'] == "reserva_gratis":
                            remate_wa = "Acepto los términos y la tolerancia de 30 minutos de espera. ¡Nos vemos allá! 🎤"
                            texto_instruccion_wa = "Para validar y guardar tu mesa de forma definitiva, presiona el botón verde de abajo para notificarnos vía WhatsApp."
                        else:
                            remate_wa = "Acepto los términos de abono consumible y políticas de cancelación 24h. Adjunto comprobante de transferencia de $10.000. 👇"
                            texto_instruccion_wa = "Para validar tu abono consumible, presiona el botón de abajo para abrir WhatsApp y <b>enviarnos la captura del comprobante</b>."

                        mensaje_wa = (
                            f"¡Hola! 🍹 Acabo de registrar una reserva desde la Ticketera Web.\n\n"
                            f"👤 *Nombre:* {nombre}\n"
                            f"🆔 *RUT:* {rut}\n"
                            f"📅 *Evento:* {ev['titulo']}\n"
                            f"🪑 *Mesa:* {mesa_seleccionada}\n\n"
                            f"{remate_wa}"
                        )

                        mensaje_codificado = requests.utils.quote(mensaje_wa)
                        url_whatsapp = f"https://wa.me/56996777779?text={mensaje_codificado}"

                        st.markdown(f"""
                            <div style="background-color: #ff007f1a; padding: 15px; border-radius: 8px; border: 1px dashed #ff007f; margin-bottom: 15px;">
                                <p style="margin: 0; color: #ff007f; font-weight: bold; text-align: center;">⚠️ ¡ÚLTIMO PASO OBLIGATORIO! ⚠️</p>
                                <p style="margin: 5px 0 0 0; font-size: 14px; text-align: center;">{texto_instruccion_wa}</p>
                            </div>
                        """, unsafe_allow_html=True)

                        st.link_button("🟢 Notificar Reserva por WhatsApp", url_whatsapp, type="primary", use_container_width=True)
                    else:
                        st.error(f"Error de comunicación con el servidor (Código {respuesta.status_code}).")
                except Exception as e:
                    st.error(f"Error al procesar la reserva: {e}")
            else:
                st.warning("Por favor, rellena tu Nombre y tu RUT antes de enviar la solicitud.")
    else:
        st.warning("📍 Este evento no requiere reserva previa de mesas. ¡Te esperamos por orden de llegada al local!")
