
from flask import Blueprint, jsonify
from app.services.correo import enviar_recordatorio


test_correo_bp = Blueprint(
    "test_correo",
    __name__,
    url_prefix="/test"
)


@test_correo_bp.route("/correo")
def test_correo():

    enviar_recordatorio(
        "Prueba Attendix",
        "jeinerramirez1910@gmail.com"
    )

    return jsonify({
        "mensaje": "Correo enviado correctamente"
    })


import socket

@test_correo_bp.route("/smtp")
def test_smtp():

    servidor = "smtp.gmail.com"
    puerto = 587

    try:
        socket.create_connection(
            (servidor, puerto),
            timeout=10
        )

        return {
            "estado": "OK",
            "mensaje": "Render puede conectarse a smtp.gmail.com:587"
        }

    except Exception as e:

        return {
            "estado": "ERROR",
            "mensaje": str(e)
        }, 500
