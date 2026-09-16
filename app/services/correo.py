from flask_mail import Message
from flask import render_template
from app.extensions import mail


def enviar_recordatorio(nombre, correo):

    mensaje = Message(
        subject="Recordatorio de cierre de jornada",
        recipients=[correo]
    )

    mensaje.html = render_template(
        "emails/cierre_jornada.html",
        nombre=nombre
    )

    mail.send(mensaje)
