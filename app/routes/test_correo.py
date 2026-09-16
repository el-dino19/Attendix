
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
        "attendix.notificacion@gamil.com"
    )

    return jsonify({
        "mensaje": "Correo enviado correctamente"
    })
