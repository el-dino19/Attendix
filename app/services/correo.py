import os
import resend


resend.api_key = os.getenv("RESEND_API_KEY")


def enviar_recordatorio(nombre, correo):

    resend.Emails.send({
        "from": "Attendix <onboarding@resend.dev>",
        "to": [correo],
        "subject": "Recordatorio de cierre de jornada",
        "html": f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
        </head>

        <body>

            <h2>Recordatorio de cierre de jornada</h2>

            <p>Hola <strong>{nombre}</strong>.</p>

            <p>
                Han transcurrido <strong>8 horas</strong>
                desde el inicio de tu jornada laboral.
            </p>

            <p>
                Por favor ingresa al sistema y realiza
                el cierre de tu jornada.
            </p>

            <p>Gracias.</p>

        </body>
        </html>
        """
    })
