from app import bcrypt
from app.models.usuario import Usuario


def autenticar_usuario(correo, password):
    usuario = Usuario.query.filter_by(
        correo=correo
    ).first()

    if usuario is None:
        return None

    if not usuario.activo:
        return None

    if not bcrypt.check_password_hash(
        usuario.password_hash,
        password
    ):
        return None

    return usuario