# ==============================================================================
# BASE DE DATOS DE EVENTOS (Actualizada a Markdown Nativo)
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
1. **Entrada Liberada:** No se cobra abono previo para este evento.
2. **Tolerancia de espera:** La mesa se reserva **solo por 30 minutos** desde el inicio del evento (hasta las 22:30 hrs). Pasado ese tiempo, la mesa quedará libre para el público general.
3. **Propina:** Te invitamos a dejarle una propina voluntaria a la animadora para apoyar el karaoke en vivo.
        """,
        "precio_min": "$0"
    },
    {
        "id": "tiktu_01",
        "titulo": "Tiktuarawitaki en vivo: poesía, música e ilustración en una experiencia única",
        "fecha": "Viernes 03 de Julio",
        "hora": "21:00 hrs",
        "tipo": "reserva_pago",
        "descripcion": """Te invitamos a ser parte de una presentación especial de Tiktuarawitaki: Revitalizando la Herencia Cultural 🎨📖🎶

Una experiencia interdisciplinaria que une dibujo en vivo, poesía y música, inspirada en la obra de Gabriela Mistral y Manuel Rojas, donde la palabra, la imagen y el sonido se encuentran para dar vida a una nueva mirada sobre nuestra memoria cultural.

Esta presentación tiene además un propósito muy especial: reunir fondos para nuestra participación en una próxima presentación en Buenos Aires, llevando esta propuesta chilena a nuevos espacios de encuentro artístico y cultural. 🇨🇱✨""",
        "datos_pago": {
            "banco": "BancoEstado (CuentaRUT)",
            "cuenta": "11.633.847-5",
            "monto": "$10.000 (Abono transferido)",
            "correo": "clubrepiola@gmail.com"
        },
        "politicas": """
1. **Abono Consumible:** El valor de la reserva es de **$10.000**, los cuales se descontarán en su totalidad de tu consumo total en el local.
2. **Política de Cancelación:** Si avisas con un mínimo de **24 horas de anticipación**, se te devolverá el 100% del dinero. Si avisas tarde o no avisas, **no habrá devolución**.
3. **Tolerancia de espera:** La mesa se guardará **solo por 30 minutos** iniciado el evento (hasta las 21:30 hrs). Pasado ese tiempo, la mesa se liberará para el público general.
        """,
        "precio_min": "🎟️ Adhesión voluntaria desde $3.000"
    },
    {
        "id": "promo_jueves",
        "titulo": "Jueves de Poesía",
        "fecha": "Todos los Jueves",
        "hora": "18:00 a 24:00 hrs",
        "tipo": "solo_info",
        "descripcion": "Todos los Jueves tenemos Poesía Clandestina. ¡Trae a tus amigos y disfruta de la mejor poesía!",
        "politicas": "* Ingreso por orden de llegada.",
        "precio_min": "Solo Info"
    }
]
