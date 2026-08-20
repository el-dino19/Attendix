from flask import Blueprint
from app.models.usuario import Usuario


test_bp = Blueprint(
    "test",
    __name__,
    url_prefix="/test"
)


@test_bp.route("/usuarios")
def usuarios():

    lista_usuarios = Usuario.query.all()

    resultado = []

    for usuario in lista_usuarios:
        resultado.append({
            "id": usuario.id,
            "nombre": usuario.nombre,
            "correo": usuario.correo,
            "rol": usuario.rol,
            "activo": usuario.activo
        })

    return resultado