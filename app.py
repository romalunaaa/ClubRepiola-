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
    page_title="Club Repiola - Reservas", page_icon="🍹", layout="centered"
)

# ==============================================================================
# 1. BARRA LATERAL (BRANDBOARD E INFORMACIÓN DE LA PYME)
# ==============================================================================
with st.sidebar:
    try:
        st.image("logorepiola.jpg", use_container_width=True)
    except:
        st.subheader("🎵 Club Repiola Bar")

    st.markdown("---")
    st.markdown("### 🕒 Horario Otoño")
    st.write("• **Jueves:** 18:00 a 24:00 hrs")
    st.write("• **Viernes y Sábado:** 18:00 a 03:00 hrs")
    st.write("• **Domingo:** Solo Eventos reservados.")

    st.markdown("---")
    st.markdown("### 📍 Ubicación")
    st.caption("Vicuña Rozas 5032, Quinta Normal, Santiago, Chile")

    st.markdown("---")
    st.markdown("### 📞 Contacto Soporte")
    st.success("[WhatsApp +56 9 9677 7779](https://wa.me/56996777779)")


# ==============================================================================
# 2. CUERPO PRINCIPAL DE LA APP
# ==============================================================================
st.title("🍹 Reserva tu Mesa en Club Repiola")
st.markdown(
    "Asegura tu espacio completando el formulario. Los cupos son limitados."
)
st.write("---")

st.info(
    "💡 **Dato Repiola:** Las reservas se mantienen hasta 20 minutos después de la hora acordada."
)

st.write("") 

# Tarjeta informativa CuentaRUT BancoEstado + POLÍTICAS DE ABONO CLARAS
st.markdown(
    """
<div style="background-color: #1e1a3a; padding: 20px; border-radius: 10px; border: 1px solid #ff007f;">
    <h4 style="color: #ff007f; margin-top:0;">💳 Datos de Abono (CuentaRUT):</h4>
    <p style="margin-bottom: 10px;">Realiza la transferencia para congelar tu mesa de forma inmediata:</p>
    <ul style="margin-bottom: 15px;">
        <li><b>Banco:</b> BancoEstado (CuentaRUT)</li>
        <li><b>Número de Cuenta:</b> 96777779 <i>(RUT del bar sin guion)</i></li>
        <li><b>Monto Abono:</b> $10.000</li>
        <li><b>Correo:</b> contacto@clubrepiola.cl</li>
    </ul>
    <h4 style="color: #ff007f; margin-top:15px; margin-bottom:5px;">⚠️ ¿Cómo funciona el Abono? (Términos y Condiciones):</h4>
    <ol style="font-size: 14px;">
        <li><b>¡Se descuenta de tu cuenta!</b> Al asistir al bar, los $10.000 de abono se rebajarán del total de lo que consuman esa noche.</li>
        <li><b>Cancelación con aviso (1 día antes):</b> Si por cualquier motivo no puedes asistir y nos avisas con al menos 24 horas de anticipación, te devolveremos el 100% de tu dinero.</li>
        <li><b>Inasistencia sin aviso:</b> Si no avisas con la anticipación debida o el grupo no se presenta (No-Show), el dinero del abono <b>no será reembolsable</b> por concepto de reserva y bloqueo de mesa.</li>
    </ol>
</div>
""",
    unsafe_allow_html=True,
)

st.write("")

# ==============================================================================
# 3. FORMULARIO DE RESERVA
# ==============================================================================
with st.form("formulario_reserva"):
    st.subheader("✨ Completa tus datos")

    # Selección de eventos
    evento_seleccionado = st.selectbox(
        "Selecciona el Evento / Fecha",
        [
            "Viernes de Karaoke (18:00 hrs)",
            "Sábado Club General (18:00 hrs)",
            "Evento Especial - Lanzamiento",
        ],
    )

    # 📝 DESCRIPCIONES DINÁMICAS SEGÚN EL EVENTO SELECCIONADO
    if evento_seleccionado == "Viernes de Karaoke (18:00 hrs)":
        st.markdown("*🎤 **Sobre este evento:** ¡Saca el artista que llevas dentro! Una noche cargada de buena música, promociones en schops y tragos tradicionales. Ideal para venir con amigos del trabajo o celebrar cumpleaños en un ambiente ultra prendido.*")
    elif evento_seleccionado == "Sábado Club General (18:00 hrs)":
        st.markdown("*🎧 **Sobre este evento:** Nuestra gran noche bailable. El mejor DJ de la zona mezclando hits urbanos, reggaetón de la vieja escuela, pop y electrónica. Sonido e iluminación de alta fidelidad. ¡La pista de baile se enciende temprano!*")
    elif evento_seleccionado == "Evento Especial - Lanzamiento":
        st.markdown("*🚀 **Sobre este evento:** Una jornada única con degustaciones exclusivas de nuestra nueva carta de coctelería de autor, sorpresas en vivo y regalos para las primeras mesas en llegar. ¡Cupos muy limitados!*")

    st.write("")

    mesa_seleccionada = st.selectbox(
        "Selecciona tu Mesa preferida",
        ["Mesa Vip 1", "Mesa Vip 2", "Mesa General A", "Mesa General B", "Terraza 1"],
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

                # Generar el mensaje automático para WhatsApp
                mensaje_wa = (
                    f"¡Hola! 🍹 Acabo de registrar una reserva en la web.\n\n"
                    f"👤 *Nombre:* {nombre}\n"
                    f"🆔 *RUT:* {rut}\n"
                    f"📅 *Evento:* {evento_seleccionado}\n"
                    f"🪑 *Mesa:* {mesa_seleccionada}\n\n"
                    f"Acepto las políticas de reserva. Aquí adjunto el comprobante de transferencia por los $10.000. 👇"
                )

                mensaje_codificado = requests.utils.quote(mensaje_wa)
                url_whatsapp = f"https://wa.me/56996777779?text={mensaje_codificado}"

                # Cuadro de advertencia claro
                st.markdown(
                    """
                <div style="background-color: #ff007f1a; padding: 15px; border-radius: 8px; border: 1px dashed #ff007f; margin-bottom: 15px;">
                    <p style="margin: 0; color: #ff007f; font-weight: bold; text-align: center;">
                        ⚠️ ¡ÚLTIMO PASO OBLIGATORIO! ⚠️
                    </p>
                    <p style="margin: 5px 0 0 0; font-size: 14px; text-align: center;">
                        Para validar tu abono y confirmar tu mesa, presiona el botón verde de abajo para abrir WhatsApp y <b>enviarnos la captura del comprobante</b>.
                    </p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # Botón llamativo para saltar a WhatsApp
                st.link_button(
                    "🟢 Enviar Comprobante por WhatsApp",
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
