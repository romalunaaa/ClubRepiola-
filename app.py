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
# REEMPLAZO DEL TÍTULO POR TU IMAGEN DE TÍTULO
try:
    # Asegúrate de guardar tu imagen de título con este nombre en la misma carpeta
    st.image("titulo_repiola.png", use_container_width=True)
except:
    # Respaldo en texto plano si la imagen no se encuentra
    st.title("Club Repiola")

st.subheader("Reserva tu Mesa")
st.markdown(
    "Asegura tu espacio completando el formulario. Los cupos son limitados combinando música, ritmo y buena vibra."
)
st.write("---")

# Secciones de alertas limpias, sin iconos
st.info("**Dato Repiola:** Las reservas se mantienen hasta 30 minutos después de la hora acordada.")
st.warning("Cupos Limitados. Viernes y Sábados los cupos se llenan rápido.")

st.write("") 

# Tarjeta de transferencia limpia, sin imágenes superiores ni iconos internos
st.markdown(
    """
<div style="background-color: #1A1A1A; padding: 20px; border-radius: 12px; border: 2px solid #E11D74; box-shadow: 0px 4px 15px rgba(225, 29, 116, 0.2);">
    <h4 style="color: #FFD31D; margin-top:0; font-family: sans-serif; letter-spacing: 1px;">Instrucciones de Abono (CuentaRUT):</h4>
    <p style="margin-bottom: 15px; color: #FFFFFF;">Realiza la transferencia para congelar tu mesa de forma inmediata con toda la onda:</p>
    <ul style="color: #00A8CC; list-style-type: square;">
        <li><b style="color: #FFFFFF;">Banco:</b> BancoEstado (CuentaRUT)</li>
        <li><b style="color: #FFFFFF;">Número de Cuenta:</b> 11.633.847-5</li>
        <li><b style="color: #FFFFFF;">Monto Abono:</b> $10.000</li>
        <li><b style="color: #FFFFFF;">Correo:</b> clubrepiola@gmail.com</li>
    </ul>
</div>
""",
    unsafe_allow_html=True,
)

st.write("")

# ==============================================================================
# 3. FORMULARIO DE RESERVA
# ==============================================================================
with st.form("formulario_reserva"):
    st.subheader("Completa tus datos")

    evento_seleccionado = st.selectbox(
        "Selecciona el Evento / Fecha",
        [
            "Jueves de Poesía (21:00 hrs)",
            "Viernes de Karaoke (22:00 hrs)",
            "Evento Especial - Lanzamiento Repiola",
        ],
    )

    mesa_seleccionada = st.selectbox(
        "Selecciona tu Mesa preferida",
        ["Mesa para 1", "Mesa para 2", "Terraza(Exterior)", "Mesa para 3"],
    )

    nombre = st.text_input("Nombre Completo de quien asiste")
    rut = st.text_input("RUT del Titular (Para validar transferencia)")

    boton_confirmar = st.form_submit_button("Enviar y Congelar Mesa")


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

            respuesta = requests.post(url_formulario, data=datos_reserva_forms)

            if respuesta.status_code == 200:
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
                st.success("¡Datos registrados con éxito!")

                mensaje_wa = (
                    f"¡Hola! Acabo de registrar una reserva en Club Repiola.\n\n"
                    f"👤 *Nombre:* {nombre}\n"
                    f"🆔 *RUT:* {rut}\n"
                    f"📅 *Evento:* {evento_seleccionado}\n"
                    f"🪑 *Mesa:* {mesa_seleccionada}\n\n"
                    f"Aquí adjunto el comprobante de transferencia."
                )

                mensaje_codificado = requests.utils.quote(mensaje_wa)
                url_whatsapp = f"https://wa.me/56996777779?text={mensaje_codificado}"

                st.markdown(
                    """
                <div style="background-color: rgba(225, 29, 116, 0.1); padding: 15px; border-radius: 8px; border: 1px dashed #E11D74; margin-bottom: 15px;">
                    <p style="margin: 0; color: #E11D74; font-weight: bold; text-align: center;">
                        ⚠️ ¡ÚLTIMO PASO OBLIGATORIO! ⚠️
                    </p>
                    <p style="margin: 5px 0 0 0; font-size: 14px; text-align: center; color: #FFFFFF;">
                        Para validar tu abono y confirmar tu mesa, presiona el botón de abajo para abrir WhatsApp y <b>enviarnos la captura del comprobante</b>.
                    </p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                st.link_button(
                    "Enviar Comprobante por WhatsApp",
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