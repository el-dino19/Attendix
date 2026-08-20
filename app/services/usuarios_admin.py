from app import db, bcrypt
from app.models.usuario import Usuario


# ==========================================
# OBTENER TODOS LOS USUARIOS
# ==========================================

def obtener_usuarios():

    return Usuario.query.order_by(
        Usuario.nombre.asc()
    ).all()


# ==========================================
# CREAR USUARIO
# ==========================================

def crear_usuario(
    nombre,
    correo,
    password,
    rol="empleado"
):

    # --------------------------------------
    # VERIFICAR CORREO
    # --------------------------------------

    existente = Usuario.query.filter_by(
        correo=correo
    ).first()

    if existente:

        return (
            False,
            "El correo ya está registrado.",
            None
        )


    # --------------------------------------
    # GENERAR PASSWORD
    # --------------------------------------

    password_hash = bcrypt.generate_password_hash(
        password
    ).decode("utf-8")


    # --------------------------------------
    # CREAR USUARIO
    # --------------------------------------

    usuario = Usuario(
        nombre=nombre,
        correo=correo,
        password_hash=password_hash,
        activo=True,
        rol=rol
    )


    db.session.add(usuario)

    db.session.commit()


    return (
        True,
        "Usuario creado correctamente.",
        usuario
    )


# ==========================================
# EDITAR USUARIO
# ==========================================

def editar_usuario(
    usuario_id,
    nombre,
    correo,
    rol
):

    usuario = Usuario.query.get(
        usuario_id
    )


    if usuario is None:

        return (
            False,
            "Usuario no encontrado.",
            None
        )


    # --------------------------------------
    # VERIFICAR CORREO
    # --------------------------------------

    existente = Usuario.query.filter(
        Usuario.correo == correo,
        Usuario.id != usuario_id
    ).first()


    if existente:

        return (
            False,
            "El correo ya pertenece a otro usuario.",
            None
        )


    usuario.nombre = nombre
    usuario.correo = correo
    usuario.rol = rol


    db.session.commit()


    return (
        True,
        "Usuario actualizado correctamente.",
        usuario
    )


# ==========================================
# CAMBIAR PASSWORD
# ==========================================

def cambiar_password(
    usuario_id,
    password
):

    usuario = Usuario.query.get(
        usuario_id
    )


    if usuario is None:

        return (
            False,
            "Usuario no encontrado."
        )


    usuario.password_hash = (
        bcrypt.generate_password_hash(
            password
        ).decode("utf-8")
    )


    db.session.commit()


    return (
        True,
        "Contraseña actualizada correctamente."
    )


# ==========================================
# ACTIVAR / DESACTIVAR
# ==========================================

def cambiar_estado_usuario(
    usuario_id
):

    usuario = Usuario.query.get(
        usuario_id
    )


    if usuario is None:

        return (
            False,
            "Usuario no encontrado."
        )


    usuario.activo = not usuario.activo


    db.session.commit()


    if usuario.activo:

        mensaje = "Usuario activado correctamente."

    else:

        mensaje = "Usuario desactivado correctamente."


    return (
        True,
        mensaje
    )