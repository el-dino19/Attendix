from app import db
from app.models.usuario import Usuario
from app.models.grupo import Grupo
from app.models.grupo_miembro import GrupoMiembro


def obtener_grupos_usuario(usuario_id, solo_activos=True):
    query = (
        Grupo.query
        .join(GrupoMiembro)
        .filter(
            GrupoMiembro.usuario_id == usuario_id,
            GrupoMiembro.activo.is_(True)
        )
    )
    if solo_activos:
        query = query.filter(Grupo.activo.is_(True))
    return query.order_by(Grupo.nombre.asc()).all()


def es_miembro(grupo_id, usuario_id, roles=None):
    query = GrupoMiembro.query.filter_by(
        grupo_id=grupo_id,
        usuario_id=usuario_id,
        activo=True
    )
    if roles:
        query = query.filter(GrupoMiembro.rol.in_(roles))
    return query.first() is not None


def es_admin_grupo(grupo_id, usuario_id):
    return es_miembro(grupo_id, usuario_id, ["admin"])


def obtener_membresia(grupo_id, usuario_id):
    return GrupoMiembro.query.filter_by(
        grupo_id=grupo_id,
        usuario_id=usuario_id,
        activo=True
    ).first()


def crear_grupo(nombre, descripcion, creador_id):
    nombre = (nombre or "").strip()
    descripcion = (descripcion or "").strip() or None

    if not nombre:
        return False, "El nombre del grupo es obligatorio.", None

    if Grupo.query.filter_by(nombre=nombre).first():
        return False, "Ya existe un grupo con ese nombre.", None

    creador = Usuario.query.get(creador_id)
    if creador is None or not creador.activo:
        return False, "El creador del grupo no es válido.", None

    grupo = Grupo(
        nombre=nombre,
        descripcion=descripcion,
        creado_por=creador_id,
        activo=True
    )

    db.session.add(grupo)
    db.session.flush()

    db.session.add(
        GrupoMiembro(
            grupo_id=grupo.id,
            usuario_id=creador_id,
            rol="admin",
            activo=True
        )
    )

    db.session.commit()

    return True, "Grupo creado correctamente.", grupo


def agregar_miembro(grupo_id, usuario_id, rol="colaborador"):
    if rol not in ("admin", "colaborador"):
        return False, "Rol de grupo inválido.", None

    grupo = Grupo.query.get(grupo_id)
    usuario = Usuario.query.get(usuario_id)

    if not grupo or not grupo.activo:
        return False, "El grupo no existe o está inactivo.", None

    if not usuario or not usuario.activo:
        return False, "El usuario no existe o está inactivo.", None

    miembro = GrupoMiembro.query.filter_by(
        grupo_id=grupo_id,
        usuario_id=usuario_id
    ).first()

    if miembro:
        miembro.rol = rol
        miembro.activo = True
    else:
        miembro = GrupoMiembro(
            grupo_id=grupo_id,
            usuario_id=usuario_id,
            rol=rol,
            activo=True
        )
        db.session.add(miembro)

    db.session.commit()

    return True, "Membresía actualizada correctamente.", miembro


def quitar_miembro(grupo_id, usuario_id):
    miembro = GrupoMiembro.query.filter_by(
        grupo_id=grupo_id,
        usuario_id=usuario_id
    ).first()

    if not miembro or not miembro.activo:
        return False, "El usuario no pertenece al grupo."

    if miembro.rol == "admin":
        admins = GrupoMiembro.query.filter_by(
            grupo_id=grupo_id,
            rol="admin",
            activo=True
        ).count()

        if admins <= 1:
            return False, "El grupo debe conservar al menos un administrador."

    miembro.activo = False
    db.session.commit()

    return True, "Usuario retirado del grupo correctamente."


def cambiar_rol_miembro(grupo_id, usuario_id, nuevo_rol):
    if nuevo_rol not in ("admin", "colaborador"):
        return False, "Rol de grupo inválido."

    miembro = GrupoMiembro.query.filter_by(
        grupo_id=grupo_id,
        usuario_id=usuario_id,
        activo=True
    ).first()

    if not miembro:
        return False, "El usuario no pertenece al grupo."

    if miembro.rol == "admin" and nuevo_rol == "colaborador":
        admins = GrupoMiembro.query.filter_by(
            grupo_id=grupo_id,
            rol="admin",
            activo=True
        ).count()

        if admins <= 1:
            return False, "El grupo debe conservar al menos un administrador."

    miembro.rol = nuevo_rol
    db.session.commit()

    return True, "Rol del grupo actualizado correctamente."


def listar_miembros(grupo_id):
    return (
        GrupoMiembro.query
        .join(Usuario)
        .filter(
            GrupoMiembro.grupo_id == grupo_id,
            GrupoMiembro.activo.is_(True)
        )
        .order_by(Usuario.nombre.asc())
        .all()
    )


def grupos_administrados(usuario_id):
    return (
        Grupo.query
        .join(GrupoMiembro)
        .filter(
            GrupoMiembro.usuario_id == usuario_id,
            GrupoMiembro.rol == "admin",
            GrupoMiembro.activo.is_(True),
            Grupo.activo.is_(True)
        )
        .order_by(Grupo.nombre.asc())
        .all()
    )
