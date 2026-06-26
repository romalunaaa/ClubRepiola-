# ==============================================================================
# PARCHE DE COMPATIBILIDAD PYTHON 3.13 + STREAMLIT
# ==============================================================================
import builtins
import importlib
import os
import sys

if not hasattr(builtins, "sys"):
    builtins.sys = sys
if "sys" not in sys.modules:
    sys.modules["sys"] = sys

from datetime import datetime
import pandas as pd
import requests
import streamlit as st

# ==============================================================================
# CONFIGURACIÓN DE PÁGINA DE STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="Club Repiola - Reservas", layout="centered"
)

# ==============================================================================
# CONTROLLER / ESTADO DE LA APP (Para manejo dinámico de eventos)
# ==============================================================================
OPCIONES_EVENTOS = [
    "Sábado de Karaoke (22:00 hrs)",
    "Viernes 03 de julio Tiktuarawitaki en vivo (21:00 hrs)",
]

if "evento_actual" not in st.session_state:
    st.session_state.evento_actual = OPCIONES_EVENTOS[0]

# ==============================================================================
# 1. BARRA LATERAL (BRANDBOARD E INFORMACIÓN DE LA PYME)
# ==============================================================================
with st.sidebar:
    try:
        st.image("logorepiola.jpg", use_container_width=True)
    except:
        st.subheader("Club Repiola")

    st.markdown("---")
    
    # Horario con icono predeterminado
    st.markdown("### 🕒 Horario Otoño")
    st.write("• **Jueves:** 18:00 a 24:00 hrs")
    st.write("• **Viernes y Sábado:** 18:00 a 03:00 hrs")
    st.write("• **Domingo:** Solo Eventos reservados.")

    st.markdown("---")
    
    # Ubicación con icono predeterminado
    st.markdown("### 📍 Ubicación")
    st.caption("Vicuña Rozas 5032, Quinta Normal, Santiago, Chile")

    st.markdown("---")
    
    # WhatsApp con icono predeterminado
    st.markdown("### 📞 WhatsApp")
    st.success("[+56 9 9677 7779](https://wa.me/56996777779)")


# ==============================================================================
# 2. CUERPO PRINCIPAL DE LA APP
# ==============================================================================
try:
    # Asegúrate de guardar tu imagen de título con este nombre en la misma carpeta
    st.image("titulo_repiola.png", use_container_width=True)
except:
    # Respaldo en texto plano si la imagen no se encuentra
    st.title("Club Repiola")

st.subheader("Reserva tu Mesa")
st.markdown(
    "Asegura tu espacio completando el formulario. Los cupos son limitados."
)
st.write("---")

# Secciones de alertas limpias, sin iconos
st.info("**Dato Repiola:** Las reservas se mantienen hasta 30 minutos después de la hora acordada.")
st.warning("Cupos Limitados. Viernes y Sábados los cupos se llenan rápido.")
st.info("**¡Hola! Te contamos:** Para aprovechar al máximo nuestro espacio, algunas de nuestras mesas se comparten con otros clientes. Tenlo en consideración al hacer tu reserva.")

st.write("")

# LÓGICA DE DATOS DINÁMICOS PARA LA TARJETA DE TRANSFERENCIA (Sin espacios al inicio)
evento_leyendo = st.session_state.evento_actual

if evento_leyendo == "Sábado de Karaoke (22:00 hrs)":
    titulo_tarjeta = "Información de Acceso (Entrada Liberada):"
    bajada_tarjeta = "Para este evento no necesitas realizar abonos previos de dinero:"
    cuerpo_tarjeta = '<li><b style="color: #FFFFFF;">Costo de Reserva:</b> Gratis / $0</li><li><b style="color: #FFFFFF;">Acceso:</b> Solo debes asegurar tu cupo completando el formulario de abajo.</li>'
    politicas_tarjeta = '<li><b>¡Entrada Liberada!</b> No se cobra abono de mesa previa.</li><li><b>Apoya el arte local:</b> Te invitamos a dejarle una propina con toda la buena vibra a la animadora que estará prendiendo el karaoke en vivo.</li>'
else:
    # Caso: Viernes 03 de julio Tiktuarawitaki en vivo (21:00 hrs)
    titulo_tarjeta = "Instrucciones de Adhesión (CuentaRUT):"
    bajada_tarjeta = "Realiza la transferencia para congelar tu espacio de forma inmediata con toda la onda:"
    cuerpo_tarjeta = '<li><b style="color: #FFFFFF;">Banco:</b> BancoEstado (CuentaRUT)</li><li><b style="color: #FFFFFF;">Número de Cuenta:</b> 11.633.847-5</li><li><b style="color: #FFFFFF;">Monto Adhesión:</b> Voluntaria desde $3.000</li><li><b style="color: #FFFFFF;">Correo:</b> clubrepiola@gmail.com</li>'
    politicas_tarjeta = '<li><b>Propósito Especial:</b> Todo lo recaudado por concepto de adhesión voluntaria va directamente a financiar la presentación de este proyecto artístico✨</li><li><b>Validación:</b> Es importante ingresar el RUT del titular de la transferencia para validar correctamente tu aporte.</li>'

# Tarjeta de transferencia armada en una sola línea de HTML para evitar que Streamlit rompa el diseño
html_tarjeta = f"""<div style="background-color: #1A1A1A; padding: 20px; border-radius: 12px; border: 2px solid #E11D74; box-shadow: 0px 4px 15px rgba(225, 29, 116, 0.2);"><h4 style="color: #FFD31D; margin-top:0; font-family: sans-serif; letter-spacing: 1px;">{titulo_tarjeta}</h4><p style="margin-bottom: 15px; color: #FFFFFF;">{bajada_tarjeta}</p><ul style="color: #00A8CC; list-style-type: square;">{cuerpo_tarjeta}</ul><h4 style="color: #ff007f; margin-top:15px; margin-bottom:5px;">⚠️ Detalles del Evento (Términos y Condiciones):</h4><ol style="font-size: 14px; color: #FFFFFF;">{politicas_tarjeta}</ol></div>"""

st.markdown(html_tarjeta, unsafe_allow_html=True)

st.write("")

# ==============================================================================
# 3. FORMULARIO DE RESERVA
# ==============================================================================
# Selector fuera del form para refrescar la tarjeta superior al hacer click
evento_seleccionado = st.selectbox(
    "Selecciona el Evento / Fecha",
    OPCIONES_EVENTOS,
    key="selectbox_evento"
)

# Sincronizamos cambios inmediatos
if st.session_state.selectbox_evento != st.session_state.evento_actual:
    st.session_state.evento_actual = st.session_state.selectbox_evento
    st.rerun()

with st.form("formulario_reserva"):
    st.subheader("Completa tus datos")

    # 📝 DESCRIPCIONES DINÁMICAS SEGÚN EL EVENTO SELECCIONADO
    if evento_seleccionado == "Sábado de Karaoke (22:00 hrs)":
        st.markdown("*🎤 **Sobre este evento:** ¡Saca el artista que llevas dentro! Una noche cargada de buena música y ruletas con premios. Ideal para venir con amigos del trabajo o celebrar cumpleaños en un ambiente ultra prendido.*")
    elif evento_seleccionado == "Viernes 03 de julio Tiktuarawitaki en vivo (21:00 hrs)":
        st.markdown("""*🎧 **Te invitamos a ser parte de una presentación especial de Tiktuarawitaki: Revitalizando la Herencia Cultural 🎨📖🎶**

Una experiencia interdisciplinaria que une dibujo en vivo, poesía y música, inspirada en la obra de Gabriela Mistral y Manuel Rojas, donde la palabra, la imagen y el sonido se encuentran para dar vida a una nueva mirada sobre nuestra memoria cultural.

Esta presentación tiene además un propósito muy especial: reunir fondos para nuestra participación en una próxima presentación en Buenos Aires, llevando esta propuesta chilena a nuevos espacios de encuentro artístico y cultural. 🇨🇱✨*""")
    
    st.write("")

    mesa_seleccionada = st.selectbox(
        "Selecciona tu Mesa preferida",
        ["Mesa para 1", "Mesa para 2", "Mesa para 3", "Mesa para 4", "Terraza"],
    )

    nombre = st.text_input("Nombre Completo de quien asiste")
    rut = st.text_input("RUT del Titular (Para validar transferencia)")

    boton_confirmar = st.form_submit_button("🚀 Enviar y Congelar Mesa")


# ==============================================================================
# 4. LÓGICA DE ENVÍO INVISIBLE + REDIRECCIÓN A WHATSAPP
# ==============================================================================
if boton_confirmar:
    if nombre and rut:
        try:
            url_formulario = "https://docs.google.com/forms/d/e/1FAIpQLSdv66lUkibd-_FgYIajnZAw6CvBnIvsfjkL_xpeWRBluWWNyQ/formResponse"

            datos_reserva_forms = {
                "entry.2041447904": evento_seleccionado,
                "entry.44496726": mesa_seleccionada,
                "entry.970850673": nombre,
                "entry.2047753483": rut,
            }

            # Enviar textos a Google Forms de manera invisible
            respuesta = requests.post(url_formulario, data=datos_reserva_forms)

            if respuesta.status_code == 200:
                # Respaldo Local de seguridad en .csv
                datos_nueva_reserva = {
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Evento": evento_seleccionado,
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
                st.success("🎉 ¡Datos registrados con éxito!")

                # Ajuste del texto final de WhatsApp según el tipo de evento
                if evento_seleccionado == "Sábado de Karaoke (22:00 hrs)":
                    remate_wa = "Acepto las políticas de reserva. ¡Nos vemos allá para cantar con toda la energía! 🎤🔥"
                else:
                    remate_wa = "Acepto las políticas de reserva. Aquí adjunto el comprobante de transferencia por la adhesión voluntaria. 👇"

                # Generar el mensaje automático para WhatsApp
                mensaje_wa = (
                    f"¡Hola! 🍹 Acabo de registrar una reserva en la web.\n\n"
                    f"👤 *Nombre:* {nombre}\n"
                    f"🆔 *RUT:* {rut}\n"
                    f"📅 *Evento:* {evento_seleccionado}\n"
                    f"🪑 *Mesa:* {mesa_seleccionada}\n\n"
                    f"{remate_wa}"
                )

                mensaje_codificado = requests.utils.quote(mensaje_wa)
                url_whatsapp = f"https://wa.me/56996777779?text={mensaje_codificado}"

                # Cuadro de advertencia claro según el evento
                if evento_seleccionado == "Sábado de Karaoke (22:00 hrs)":
                    texto_instruccion_wa = "Para validar y confirmar tu mesa de forma definitiva, presiona el botón verde de abajo para avisarnos por WhatsApp."
                else:
                    texto_instruccion_wa = "Para validar tu abono y confirmar tu mesa, presiona el botón verde de abajo para abrir WhatsApp y <b>enviarnos la captura del comprobante</b>."

                st.markdown(
                    f"""
                <div style="background-color: #ff007f1a; padding: 15px; border-radius: 8px; border: 1px dashed #ff007f; margin-bottom: 15px;">
                    <p style="margin: 0; color: #ff007f; font-weight: bold; text-align: center;">
                        ⚠️ ¡ÚLTIMO PASO OBLIGATORIO! ⚠️
                    </p>
                    <p style="margin: 5px 0 0 0; font-size: 14px; text-align: center;">
                        {texto_instruccion_wa}
                    </p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # Botón llamativo para saltar a WhatsApp
                st.link_button(
                    "🟢 Notificar Reserva por WhatsApp",
                    url_whatsapp,
                    type="primary",
                    use_container_width=True,
                )

            else:
                st.error(f"Error de comunicación con el servidor (Código {respuesta.status_code}).")

        except Exception as e:
            st.error(f"Error al procesar la reserva: {e}")
    else:
        st.warning("Por favor, rellena tu Nombre y tu RUT antes de enviar la solicitud.")
