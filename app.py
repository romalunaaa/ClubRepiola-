import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de página de Streamlit
st.set_page_config(
    page_title="Club Repiola - Reservas",
    page_icon="🍹",
    layout="centered"
)

# ==============================================================================
# 0. CONEXIÓN DIRECTA A GOOGLE SHEETS
# ==============================================================================
sheet_id = "17yiKj6vXnbO5tYycEw4LZb_Ofr5URmitet6_1vGzIrw"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    datos_existentes = pd.read_csv(csv_url)
except Exception as e:
    st.error(f"Error al conectar con Google Sheets: {e}")
    datos_existentes = pd.DataFrame() # Respaldo vacío por si falla


# ==============================================================================
# 1. BARRA LATERAL (BRANDBOARD E INFORMACIÓN DE LA PYME)
# ==============================================================================
with st.sidebar:
    # Aquí cambiamos a "logorepiola.jpg"
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

# El título principal usará por defecto el Rosa Fuerte (primaryColor) en los detalles
st.title("🍹 Reserva tu Mesa en Club Repiola")
st.markdown("Asegura tu preventa o espacio completando el formulario. Los cupos son limitados.")
st.write("---")

# USANDO EL COLOR CELESTE: Para mensajes informativos importantes
st.info("💡 **Dato Repiola:** Las reservas se mantienen hasta 20 minutos después de la hora acordada.")

# USANDO EL COLOR AMARILLO: Para advertencias o secciones de alta atención
st.warning("⚠️ **¡Cupos Limitados!** Jueves y Sábados suelen llenarse rápido.")

# Mostrar la tabla que viene de tu Google Sheet
if not datos_existentes.empty:
    st.markdown("### 📊 Reservas Actuales")
    st.dataframe(datos_existentes)
import pandas as pd
import streamlit as st

# 1. Tu URL de Google Sheets
url = "https://docs.google.com/spreadsheets/d/17yiKj6vXnbO5tYycEw4LZb_Ofr5URmitet6_1vGzIrw/edit?usp=sharing"

# 2. Transformamos el enlace automáticamente para que sea un CSV descargable
csv_url = url.replace("/edit?usp=sharing", "/export?format=csv")

# 3. Leemos los datos directamente usando Pandas (sin usar st.connection)
datos_existentes = pd.read_csv(csv_url)

# Tarjeta informativa con los datos CuentaRUT BancoEstado
st.markdown("""
<div style="background-color: #1e1a3a; padding: 20px; border-radius: 10px; border: 1px solid #ff007f;">
    <h4 style="color: #ff007f; margin-top:0;">💳 Instrucciones de Abono (CuentaRUT):</h4>
    <p style="margin-bottom: 5px;">Realiza la transferencia para congelar tu mesa de forma inmediata:</p>
    <ul>
        <li><b>Banco:</b> BancoEstado (CuentaRUT)</li>
        <li><b>Número de Cuenta:</b> 96777779 <i>(RUT del bar sin guion)</i></li>
        <li><b>Monto Abono:</b> $10.000</li>
        <li><b>Correo:</b> contacto@clubrepiola.cl</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.write("") # Espacio en blanco

# Formulario Estilizado de Reserva
with st.form("formulario_reserva"):
    st.subheader("✨ Completa tus datos")
    
    evento_seleccionado = st.selectbox(
        "Selecciona el Evento / Fecha", 
        ["Viernes de Karaoke (18:00 hrs)", "Sábado Club General (18:00 hrs)", "Evento Especial - Lanzamiento"]
    )
    
    mesa_seleccionada = st.selectbox(
        "Selecciona tu Mesa preferida", 
        ["Mesa Vip 1", "Mesa Vip 2", "Mesa General A", "Mesa General B", "Terraza 1"]
    )
    
    nombre = st.text_input("Nombre Completo de quien asiste")
    rut = st.text_input("RUT del Titular (Para validar transferencia)")
    
    foto = st.file_uploader("📸 Sube la captura de tu transferencia BancoEstado", type=["jpg", "png", "jpeg"])
    
    boton_confirmar = st.form_submit_button("🚀 Enviar y Congelar Mesa")

# Lógica de Guardado en Sheets
if boton_confirmar:
    if nombre and rut and foto is not None:
        try:
            datos_existentes = conn.read(spreadsheet= "https://docs.google.com/spreadsheets/d/17yiKj6vXnbO5tYycEw4LZb_Ofr5URmitet6_1vGzIrw/edit?usp=sharing")
            
            nueva_reserva = pd.DataFrame([{
                "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Evento": evento_seleccionado,
                "Mesa": mesa_seleccionada,
                "Nombre": nombre,
                "RUT": rut,
                "Estado": "Pendiente"
            }])
            
            datos_actualizados = pd.concat([datos_existentes, nueva_reserva], ignore_index=True)
            conn.update(spreadsheet=URL_PLANILLA, data=datos_actualizados)
            
            st.balloons() # Animación festiva de éxito
            st.success("¡Reserva recibida! Tu mesa ya está pre-asignada. El equipo de Club Repiola validará el abono en la App de BancoEstado.")
            
        except Exception as e:
            st.error(f"Error de conexión con la base de datos: {e}")
    else:
        st.warning("Por favor, asegúrate de llenar tu nombre, RUT y cargar el comprobante antes de enviar.")