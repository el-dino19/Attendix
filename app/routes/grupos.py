from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    abort
)

from app.models import Usuario, Grupo, GrupoMiembro, Jornada
from app.services.grupos import (
    obtener_grupos_usuario,
    es_admin_grupo,
    listar_miembros,
    agregar_miembro,
    quitar_miembro,
    cambiar_rol_miembro,
    grupos_administrados
)


grupos_bp = Blueprint(
    "grupos",
    __name__,
    url_prefix="/Attendix/grupos"
)


def _puede_administrar(grupo_id):
    usuario_id = session["usuario_id"]
    return (
        session.get("rol") == "admin_global"
        or es_admin_grupo(grupo_id, usuario_id)
    )


@grupos_bp.route("/seleccionar", methods=["GET"])
def seleccionar():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    grupos = obtener_grupos_usuario(session["usuario_id"])

    if len(grupos) == 1:
        return redirect(
            url_for("grupos.seleccionar_grupo", grupo_id=grupos[0].id)
        )

    return render_template("grupos/seleccionar.html", grupos=grupos)


@grupos_bp.route("/seleccionar/<int:grupo_id>", methods=["POST"])
def seleccionar_grupo(grupo_id):
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    grupos = obtener_grupos_usuario(session["usuario_id"])
    grupo = next((g for g in grupos if g.id == grupo_id), None)

    if grupo is None:
        abort(403)

    session["grupo_id"] = grupo.id
    session["grupo_nombre"] = grupo.nombre

    if es_admin_grupo(grupo.id, session["usuario_id"]):
        session.pop("login_latitud", None)
        session.pop("login_longitud", None)
        session.pop("login_direccion", None)
        return redirect(
            url_for("grupos.dashboard", grupo_id=grupo.id)
        )

    from app.services.asistencia import registrar_entrada

    registrar_entrada(
        session["usuario_id"],
        session.get("zona_horaria", "UTC"),
        session.pop("login_latitud", None),
        session.pop("login_longitud", None),
        session.pop("login_direccion", None),
        grupo.id
    )

    return redirect(url_for("empleado.dashboard"))


@grupos_bp.route("/<int:grupo_id>")
def dashboard(grupo_id):
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    if not _puede_administrar(grupo_id):
        abort(403)

    grupo = Grupo.query.get_or_404(grupo_id)
    miembros = listar_miembros(grupo_id)

    usuarios = (
        Usuario.query
        .filter(Usuario.activo.is_(True))
        .order_by(Usuario.nombre.asc())
        .all()
    )

    return render_template(
        "grupos/dashboard.html",
        grupo=grupo,
        miembros=miembros,
        usuarios=usuarios
    )


@grupos_bp.route("/<int:grupo_id>/asistencia")
def asistencia(grupo_id):
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    if not _puede_administrar(grupo_id):
        abort(403)

    usuario_id = request.args.get("usuario_id", type=int)
    fecha_desde = request.args.get("fecha_desde")
    fecha_hasta = request.args.get("fecha_hasta")

    query = (
        Jornada.query
        .join(Usuario)
        .filter(
            Jornada.grupo_id == grupo_id,
            Usuario.rol != "admin_global"
        )
    )

    if usuario_id:
        query = query.filter(Jornada.usuario_id == usuario_id)

    if fecha_desde:
        query = query.filter(Jornada.fecha >= fecha_desde)

    if fecha_hasta:
        query = query.filter(Jornada.fecha <= fecha_hasta)

    jornadas = query.order_by(
        Jornada.fecha.desc(),
        Jornada.entrada.desc()
    ).all()

    usuarios = (
        Usuario.query
        .join(GrupoMiembro)
        .filter(
            GrupoMiembro.grupo_id == grupo_id,
            GrupoMiembro.activo.is_(True),
            Usuario.rol != "admin_global"
        )
        .order_by(Usuario.nombre.asc())
        .all()
    )

    grupo = Grupo.query.get_or_404(grupo_id)

    return render_template(
        "admin/asistencias.html",
        jornadas=jornadas,
        usuarios=usuarios,
        grupos=[grupo],
        grupo_seleccionado=grupo_id,
        asistencia_grupo=True
    )


@grupos_bp.route("/<int:grupo_id>/miembros/agregar", methods=["POST"])
def agregar(grupo_id):
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    if not _puede_administrar(grupo_id):
        abort(403)

    usuario_id = request.form.get("usuario_id", type=int)
    rol = request.form.get("rol", "colaborador")

    ok, mensaje, _ = agregar_miembro(
        grupo_id,
        usuario_id,
        rol
    )

    flash(mensaje, "success" if ok else "danger")

    return redirect(
        url_for("grupos.dashboard", grupo_id=grupo_id)
    )


@grupos_bp.route("/<int:grupo_id>/miembros/<int:usuario_id>/quitar", methods=["POST"])
def quitar(grupo_id, usuario_id):
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    if not _puede_administrar(grupo_id):
        abort(403)

    ok, mensaje = quitar_miembro(
        grupo_id,
        usuario_id
    )

    flash(mensaje, "success" if ok else "danger")

    return redirect(
        url_for("grupos.dashboard", grupo_id=grupo_id)
    )


@grupos_bp.route("/<int:grupo_id>/miembros/<int:usuario_id>/rol", methods=["POST"])
def cambiar_rol(grupo_id, usuario_id):
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    if not _puede_administrar(grupo_id):
        abort(403)

    rol = request.form.get("rol", "colaborador")

    ok, mensaje = cambiar_rol_miembro(
        grupo_id,
        usuario_id,
        rol
    )

    flash(mensaje, "success" if ok else "danger")

    return redirect(
        url_for("grupos.dashboard", grupo_id=grupo_id)
    )


@grupos_bp.route("/mis-grupos")
def mis_grupos():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("rol") == "admin_global":
        grupos = (
            Grupo.query
            .filter_by(activo=True)
            .order_by(Grupo.nombre.asc())
            .all()
        )
    else:
        grupos = obtener_grupos_usuario(session["usuario_id"])

    # Exponer el rol de la membresía para las plantillas.
    for grupo in grupos:
        membresia = GrupoMiembro.query.filter_by(
            grupo_id=grupo.id,
            usuario_id=session["usuario_id"],
            activo=True
        ).first()
        grupo.rol = (
            membresia.rol
            if membresia
            else "admin_global"
            if session.get("rol") == "admin_global"
            else "colaborador"
        )

    return render_template(
        "grupos/mis_grupos.html",
        grupos=grupos
    )
