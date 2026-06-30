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
# CONFIGURACIÓN DE PÁGINA Y ESTILOS CUSTOM (UI Premium y Limpia)
# ==============================================================================
st.set_page_config(page_title="Club Repiola - Eventos", layout="centered")

# UI/UX: Custom CSS para unificar la estética nocturna del Club sin saturar
st.markdown("""
    <style>
    /* Estilo general y fondos */
    .stApp { background-color: #0F0F12; }
    
    /* Contenedor elegante para eventos en la lista */
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
    
    /* Badges de estado discretos pero legibles */
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
    .badge-secondary { 
        background-color: #2A2A35; 
        color: #00A8CC !important; 
        padding: 4px 10px; 
        border-radius: 6px; 
        font-size: 12px; 
        font-weight: 600; 
        display: inline-block;
    }
    
    /* Caja de Datos de Transferencia en Detalle */
    .bank-box {
        background-color: #16161F;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #E11D74;
        margin: 20px 0;
    }
    
    /* Inputs y botones globales de Streamlit adaptados */
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
EVENTOS = [
    {
        "id": "tiktu_01",
        "titulo": "Tiktuarawitaki en vivo: poesía, música e ilustración",
        "fecha": "Viernes 03 de Julio de 2026",
        "hora": "21:00 hrs",
        "imagen": "image_0563da.jpeg",
        "show_info": "Entrada/Adhesión voluntaria en puerta desde $3.000",
        "descripcion": """Te invitamos a ser parte de una presentación especial de Tiktuarawitaki: Revitalizando la Herencia Cultural 🎨📖🎶

Una experiencia interdisciplinaria que une dibujo en vivo, poesía y música, inspirada en la obra de Gabriela Mistral y Manuel Rojas, donde la palabra, la imagen y el sonido se encuentran para dar vida a una nueva mirada sobre nuestra memoria cultural.

Esta presentación tiene además un propósito muy especial: reunir fondos para nuestra participación en una próxima presentación en Buenos Aires, llevando esta propuesta chilena a nuevos espacios de encuentro artístico y cultural. 🇨🇱✨""",
        "politicas": """
* **Abono Consumible:** El valor para reservar tus asientos es de **$10.000**, los cuales se descuentan en su totalidad de lo que consumas en el local.
* **Adhesión del Show:** El evento cuenta con una adhesión voluntaria en puerta sugerida desde **$3.000** destinada a los artistas.
* **Política de Cancelación:** Si avisas con un mínimo de **24 horas de anticipación**, se te devolverá el 100% del abono.
* **Tolerancia de espera:** Tus asientos se guardarán **solo por 30 minutos** iniciado el evento (hasta las 21:30 hrs).
        """
    },
    {
        "id": "soa_01",
        "titulo": "Soa Borgoña en: Salida (De todo se sale) 🎭",
        "fecha": "Sábado 04 de Julio de 2026",
        "hora": "20:00 hrs",
        "imagen": "image_0563bc.jpeg",
        "show_info": "Entrada Liberada (Aporte Voluntario al artista)",
        "descripcion": "Disfruta de una íntima y potente velada junto a Soa Borgoña en su presentación interactiva. Música, reflexiones y arte se conjugan bajo la premisa de que 'De todo se sale'. Una propuesta imperdible para comenzar el sábado por la noche.",
        "politicas": """
* **Abono Consumible:** El valor para reservar tus asientos es de **$10.000**, los cuales se descuentan en su totalidad de lo que consumas en el local.
* **Entrada Liberada:** El show no cobra una entrada fija. Te invitamos a realizar un aporte voluntario al finalizar la presentación para apoyar al artista.
* **Política de Cancelación:** Si avisas con un mínimo de **24 horas de anticipación**, se te devolverá el 100% del abono.
* **Tolerancia de espera:** Tus asientos se guardarán **solo por 30 minutos** iniciado el evento (hasta las 20:30 hrs).
        """
    },
    {
        "id": "karaoke_01",
        "titulo": "Sábado de Karaoke 🎤",
        "fecha": "Sábado 04 de Julio de 2026",
        "hora": "22:00 hrs",
        "imagen": "karaoke.jpeg",
        "show_info": "Entrada Liberada",
        "descripcion": """🇺🇸🎰 ¡CUALQUIER EXCUSA ES BUENA PARA ARMAR EL MAMBO! 🎰🇺🇸
Este sábado 4 de julio nos agarramos de la fiesta gringa para hacer un karaoke especial en Club Repiola.
🎤 La dinámica: Canta un tema en inglés o una reversión al español de un artista gringo y te ganas el derecho a tirar la ruleta. Si tienes suerte... ¡te llevas un cope gratis! 🍹🔥
🎙️ Conduce: Solo Emilia
🎛️ Produce: Estación Musical
¡Ven a cantar, jugar y pasar un sábado repiola! No te lo pierdas. ✨""",
        "politicas": """
* **Abono Consumible:** El valor para reservar tus asientos es de **$10.000**, los cuales se descuentan en su totalidad de lo que consumas en el local.
* **Entrada Liberada:** No se cobra entrada por asistir al karaoke. Te invitamos a dejarle una propina voluntaria a la animadora para apoyar el formato en vivo.
* **Política de Cancelación:** Si avisas con un mínimo de **24 horas de anticipación**, se te devolverá el 100% del abono.
* **Tolerancia de espera:** Tus asientos se guardarán **solo por 30 minutos** (hasta las 22:30 hrs).
        """
    }
]

# ==============================================================================
# MANEJO DE ESTADO
# ==============================================================================
if "vista" not in st.session_state:
    st.session_state.vista = "lista"
if "evento_sel" not in st.session_state:
    st.session_state.evento_sel = None
if "asientos_disponibles" not in st.session_state:
    st.session_state.asientos_disponibles = {ev["id"]: 35 for ev in EVENTOS}

def ir_a_detalles(evento):
    st.session_state.evento_sel = evento
    st.session_state.vista = "detalle"

def volver_a_lista():
    st.session_state.vista = "lista"
    st.session_state.evento_sel = None

# ==============================================================================
# BARRA LATERAL (INFORMACIÓN DE LA PYME - Simplificada y Elegante)
# ==============================================================================
with st.sidebar:
    try:
        st.image("logorepiola.jpg", use_container_width=True)
    except:
        st.subheader("Club Repiola")

    st.markdown("### 🕒 Horario")
    st.caption("**Jueves:** 18:00 a 24:00 hrs\n\n**Viernes y Sábado:** 18:00 a 03:00 hrs\n\n**Domingo:** Solo Eventos reservados.")

    st.markdown("---")
    st.markdown("### 📍 Ubicación")
    st.caption("Vicuña Rozas 5032, Quinta Normal, Santiago, Chile")

    st.markdown("---")
    st.markdown("### 📞 Contacto")
    st.link_button("💬 Hablar por WhatsApp", "https://wa.me/56996777779", use_container_width=True)

# ==============================================================================
# VISTA 1: HOME - EXPLORADOR DE EVENTOS (Menos ruido, Más Premium)
# ==============================================================================
if st.session_state.vista == "lista":
    try:
        st.image("titulo_repiola.png", use_container_width=True)
    except:
        st.title("Club Repiola")

    st.markdown("## Próximos Eventos")
    st.markdown("Selecciona un evento de la cartelera para ver los detalles y reservar tus asientos.")
    
    # UX: Combinamos las notas de info/warning molestas en una sola línea sutil aclaratoria
    st.markdown("> **Nota:** Todas las funciones tienen un aforo exclusivo de 35 asientos. Las reservas requieren un abono de $10.000, el cual se descontará al 100% del consumo realizado en el bar.")
    st.write("")

    for ev in EVENTOS:
        asientos_libres = st.session_state.asientos_disponibles[ev["id"]]
        
        # Tarjeta visual limpia usando HTML estructurado
        html_tarjeta = f"""
        <div class="event-card-clean">
            <div class="card-title-clean">{ev['titulo']}</div>
            <div class="card-subtitle-clean">📅 {ev['fecha']} &nbsp;&middot;&nbsp; ⏰ {ev['hora']}</div>
            <span class="badge-brand">Mesa requiere abono ($10.000)</span>
            <span class="badge-secondary">🪑 {asientos_libres} / 35 Asientos libres</span>
            <div style="margin-top: 10px; font-size: 13px; color: #8E8E93;">Acceso: {ev['show_info']}</div>
        </div>
        """
        st.markdown(html_tarjeta, unsafe_allow_html=True)
        
        # Botón nativo perfectamente integrado debajo de su tarjeta
        if st.button("Ver Información y Reservar", key=ev['id'], use_container_width=True):
            ir_a_detalles(ev)
            st.rerun()
            
        st.write("")

# ==============================================================================
# VISTA 2: PÁGINA DE DETALLE Y FORMULARIO DE RESERVA
# ==============================================================================
elif st.session_state.vista == "detalle":
    ev = st.session_state.evento_sel
    asientos_libres = st.session_state.asientos_disponibles[ev["id"]]
    
    # Botón volver discreto arriba a la izquierda
    if st.button("← Volver a la cartelera", key="btn_back"):
        volver_a_lista()
        st.rerun()

    st.write("")
    st.markdown(f"# {ev['titulo']}")
    
    if ev['imagen']:
        try:
            st.image(ev['imagen'], use_container_width=True)
        except:
            pass

    # Fila de datos rápidos del evento
    st.markdown(f"**📅 Fecha:** {ev['fecha']} | **⏰ Hora:** {ev['hora']} | **🪑 Disponibilidad:** {asientos_libres} cupos restantes")
    st.write("---")
    
    st.markdown("### Sobre este evento")
    st.markdown(ev['descripcion'])
    
    # UI: Bloque de transferencia ordenado e institucional, no chillón
    html_pago = f"""
    <div class="bank-box">
        <h4 style="color: #FFFFFF; margin-top:0; font-weight:600;">Datos de Transferencia para Reservar</h4>
        <p style="color: #A0A0AB; font-size: 14px; margin-bottom: 12px;">Para asegurar tus asientos, transfiere el abono (100% consumible en el local) a la siguiente cuenta:</p>
        <table style="width:100%; border-collapse: collapse; font-size: 14px; color: #FFF;">
            <tr><td style="padding: 4px 0; color: #8E8E93;">Banco:</td><td><b>Banco Santander (Cuenta Corriente)</b></td></tr>
            <tr><td style="padding: 4px 0; color: #8E8E93;">Rut:</td><td><b>11.633.847-5</b></td></tr>
            <tr><td style="padding: 4px 0; color: #8E8E93;">N de Cuenta:</td><td><b>0000-64583867</b></td></tr>
            <tr><td style="padding: 4px 0; color: #8E8E93;">Monto:</td><td><b>$10.000</b></td></tr>
            <tr><td style="padding: 4px 0; color: #8E8E93;">Email:</td><td><b>repiolaclub@gmail.com</b></td></tr>
        </table>
    </div>
    """
    st.markdown(html_pago, unsafe_allow_html=True)
        
    with st.expander("📝 Términos, condiciones y políticas de asistencia"):
        st.markdown(ev['politicas'])
    
    st.write("")

    # FORMULARIO DE RESERVAS
    if asientos_libres > 0:
        with st.form("formulario_reserva_dinamico"):
            st.markdown("### Completa tus datos para pre-reservar")
            st.caption("Recuerda que para validar este espacio deberás enviar el comprobante de transferencia.")
            
            max_seleccionable = min(20, asientos_libres)
            asientos_solicitados = st.selectbox(
                "¿Cuántos asientos necesitas para tu grupo?",
                list(range(1, max_seleccionable + 1)),
                format_func=lambda x: f"Mesa / Espacio para {x} persona{'s' if x > 1 else ''}"
            )

            nombre = st.text_input("Nombre completo de quien asiste")
            rut = st.text_input("RUT del titular (para validar en puerta)")

            boton_confirmar = st.form_submit_button("🚀 Enviar y Reservar Espacio", use_container_width=True)

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
                        st.success(f"🎉 ¡Pre-reserva de {asientos_solicitados} asientos registrada!")

                        # Mensaje de WhatsApp limpio y directo
                        mensaje_wa = (
                            f"¡Hola! 🍹 Acabo de registrar una reserva desde la Ticketera Web.\n\n"
                            f"👤 *Nombre:* {nombre}\n"
                            f"🆔 *RUT:* {rut}\n"
                            f"📅 *Evento:* {ev['titulo']}\n"
                            f"🪑 *Asientos:* {asientos_solicitados}\n\n"
                            f"Acepto los términos de abono consumible. Adjunto el comprobante de transferencia por $10.000 para validar."
                        )

                        mensaje_codificado = requests.utils.quote(mensaje_wa)
                        url_whatsapp = f"https://wa.me/56996777779?text={mensaje_codificado}"

                        # UX: Caja final limpia y enfocada en el CTA de WhatsApp
                        st.markdown("""
                            <div style="background-color: #16161F; padding: 15px; border-radius: 8px; border: 1px solid #E11D74; margin-bottom: 15px; text-align:center;">
                                <span style="color: #E11D74; font-weight: bold;">⚠️ ¡ÚLTIMO PASO OBLIGATORIO!</span><br>
                                <span style="font-size: 14px; color: #FFF;">Para validar tus asientos, presiona el botón de abajo y envíanos la captura de la transferencia.</span>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.link_button("🟢 Enviar Comprobante por WhatsApp", url_whatsapp, type="primary", use_container_width=True)
                        st.write("")
                        st.button("Volver al Inicio", on_click=volver_a_lista, use_container_width=True)
                        
                    else:
                        st.error(f"Error de comunicación con el servidor (Código {respuesta.status_code}).")
                except Exception as e:
                    st.error(f"Error al procesar la reserva: {e}")
            else:
                st.warning("Por favor, ingresa tu Nombre y tu RUT para continuar.")
    else:
        st.error("🚨 Lo sentimos, las reservas para este evento están AGOTADAS.")
