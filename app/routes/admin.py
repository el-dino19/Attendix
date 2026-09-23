from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    abort,
    request,
    flash,
    send_file,
)

from zoneinfo import ZoneInfo
from datetime import datetime

from app import db
from app.services.exportacion import generar_excel_asistencia
from app.models.usuario import Usuario
from app.models.jornada import Jornada
from app.models.grupo import Grupo
from app.models.grupo_miembro import GrupoMiembro

from app.services.usuarios_admin import (
    obtener_usuarios,
    crear_usuario,
    editar_usuario,
    cambiar_password,
    cambiar_estado_usuario
)

from app.services.grupos import (
    crear_grupo as crear_grupo_service,
    agregar_miembro as agregar_miembro_service,
    listar_miembros,
    cambiar_rol_miembro,
    quitar_miembro
)


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/Attendix"
)


@admin_bp.before_request
def proteger_admin():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("rol") != "admin_global":
        abort(403)


@admin_bp.route("/")
def dashboard():
    cantidad_usuarios = Usuario.query.count()
    usuarios_activos = Usuario.query.filter_by(activo=True).count()
    usuarios_inactivos = Usuario.query.filter_by(activo=False).count()
    cantidad_grupos = Grupo.query.filter_by(activo=True).count()

    return render_template(
        "admin/dashboard.html",
        cantidad_usuarios=cantidad_usuarios,
        usuarios_activos=usuarios_activos,
        usuarios_inactivos=usuarios_inactivos,
        cantidad_grupos=cantidad_grupos
    )


@admin_bp.route("/usuarios")
def usuarios():
    usuarios = obtener_usuarios()
    return render_template(
        "admin/usuarios.html",
        usuarios=usuarios
    )


@admin_bp.route("/usuarios/crear", methods=["POST"])
def crear():
    nombre = request.form.get("nombre", "").strip()
    correo = request.form.get("correo", "").strip().lower()
    password = request.form.get("password", "")
    rol = request.form.get("rol", "empleado")

    if rol == "admin":
        rol = "admin_global"

    if rol not in ("empleado", "admin_global"):
        rol = "empleado"

    usuario_existente = Usuario.query.filter_by(
        correo=correo
    ).first()

    if usuario_existente:
        flash("Ya existe un usuario registrado con ese correo.", "danger")
        return redirect(url_for("admin.usuarios"))

    if not nombre:
        flash("El nombre es obligatorio.", "danger")
        return redirect(url_for("admin.usuarios"))

    if not correo:
        flash("El correo es obligatorio.", "danger")
        return redirect(url_for("admin.usuarios"))

    if not password:
        flash("La contraseña es obligatoria.", "danger")
        return redirect(url_for("admin.usuarios"))

    exito, mensaje, _ = crear_usuario(
        nombre,
        correo,
        password,
        rol
    )

    flash(
        mensaje,
        "success" if exito else "danger"
    )

    return redirect(url_for("admin.usuarios"))


@admin_bp.route("/usuarios/<int:usuario_id>/editar", methods=["POST"])
def editar(usuario_id):
    nombre = request.form.get("nombre", "").strip()
    correo = request.form.get("correo", "").strip().lower()
    rol = request.form.get("rol", "empleado")

    if rol == "admin":
        rol = "admin_global"

    if rol not in ("empleado", "admin_global"):
        rol = "empleado"

    if not nombre or not correo:
        flash("Nombre y correo son obligatorios.", "danger")
        return redirect(url_for("admin.usuarios"))

    if usuario_id == session.get("usuario_id") and rol != "admin_global":
        flash("El administrador global actual no puede quitarse ese rol.", "danger")
        return redirect(url_for("admin.usuarios"))

    exito, mensaje, _ = editar_usuario(
        usuario_id,
        nombre,
        correo,
        rol
    )

    flash(
        mensaje,
        "success" if exito else "danger"
    )

    return redirect(url_for("admin.usuarios"))


@admin_bp.route("/usuarios/<int:usuario_id>/password", methods=["POST"])
def cambiar_password_ruta(usuario_id):
    password = request.form.get("password", "")

    if not password:
        flash("La contraseña no puede estar vacía.", "danger")
        return redirect(url_for("admin.usuarios"))

    exito, mensaje = cambiar_password(
        usuario_id,
        password
    )

    flash(
        mensaje,
        "success" if exito else "danger"
    )

    return redirect(url_for("admin.usuarios"))


@admin_bp.route("/usuarios/<int:usuario_id>/estado", methods=["POST"])
def cambiar_estado(usuario_id):
    if usuario_id == session.get("usuario_id"):
        flash("No puedes desactivar tu propio usuario.", "danger")
        return redirect(url_for("admin.usuarios"))

    exito, mensaje = cambiar_estado_usuario(usuario_id)

    flash(
        mensaje,
        "success" if exito else "danger"
    )

    return redirect(url_for("admin.usuarios"))


@admin_bp.route("/exportar")
def exportar():
    periodo = request.args.get("periodo", "todos")
    mes = request.args.get("mes", "").strip()
    grupo_id = request.args.get("grupo_id", type=int)

    query = (
        Jornada.query
        .join(Usuario)
        .filter(Usuario.rol != "admin_global")
    )

    if grupo_id:
        query = query.filter(Jornada.grupo_id == grupo_id)

    registros = query.order_by(
        Jornada.fecha.desc(),
        Jornada.entrada.desc()
    ).all()

    archivo = generar_excel_asistencia(
        registros,
        periodo=periodo,
        mes=mes
    )

    ahora = datetime.now(
        ZoneInfo("America/Bogota")
    )

    if periodo == "mes" and mes:
        nombre_archivo = f"Reporte_Asistencia_{mes}.xlsx"
    elif periodo == "3_meses":
        nombre_archivo = "Reporte_Asistencia_Ultimos_3_Meses.xlsx"
    elif periodo == "6_meses":
        nombre_archivo = "Reporte_Asistencia_Ultimos_6_Meses.xlsx"
    else:
        nombre_archivo = (
            f"Reporte_Asistencia_{ahora.strftime('%Y-%m-%d')}.xlsx"
        )

    return send_file(
        archivo,
        as_attachment=True,
        download_name=nombre_archivo,
        mimetype=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )


@admin_bp.route("/asistencia")
def asistencia():
    usuario_id = request.args.get("usuario_id", type=int)
    grupo_id = request.args.get("grupo_id", type=int)
    fecha_desde = request.args.get("fecha_desde")
    fecha_hasta = request.args.get("fecha_hasta")

    query = (
        Jornada.query
        .join(Usuario)
        .filter(Usuario.rol != "admin_global")
    )

    if grupo_id:
        query = query.filter(Jornada.grupo_id == grupo_id)

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

    usuarios_query = Usuario.query.filter(
        Usuario.rol != "admin_global"
    )

    if grupo_id:
        usuarios_query = (
            usuarios_query
            .join(GrupoMiembro)
            .filter(
                GrupoMiembro.grupo_id == grupo_id,
                GrupoMiembro.activo.is_(True)
            )
        )

    usuarios = usuarios_query.order_by(
        Usuario.nombre.asc()
    ).all()

    grupos = (
        Grupo.query
        .filter_by(activo=True)
        .order_by(Grupo.nombre.asc())
        .all()
    )

    return render_template(
        "admin/asistencias.html",
        jornadas=jornadas,
        usuarios=usuarios,
        grupos=grupos,
        grupo_seleccionado=grupo_id
    )


# =========================================================
# GRUPOS
# =========================================================

@admin_bp.route("/grupos")
def grupos():
    grupos = (
        Grupo.query
        .filter_by(activo=True)
        .order_by(Grupo.nombre.asc())
        .all()
    )

    for grupo in grupos:
        grupo.miembros_count = GrupoMiembro.query.filter_by(
            grupo_id=grupo.id,
            activo=True
        ).count()

    return render_template(
        "admin/grupos.html",
        grupos=grupos
    )


@admin_bp.route("/grupos/crear", methods=["POST"])
def crear_grupo():
    ok, mensaje, grupo = crear_grupo_service(
        request.form.get("nombre", ""),
        request.form.get("descripcion", ""),
        session["usuario_id"]
    )

    flash(
        mensaje,
        "success" if ok else "danger"
    )

    if grupo:
        return redirect(
            url_for(
                "admin.grupo_miembros",
                grupo_id=grupo.id
            )
        )

    return redirect(url_for("admin.grupos"))


@admin_bp.route("/grupos/<int:grupo_id>/miembros")
def grupo_miembros(grupo_id):
    grupo = Grupo.query.get_or_404(grupo_id)

    miembros = listar_miembros(grupo_id)

    ids = {
        miembro.usuario_id
        for miembro in miembros
    }

    usuarios_disponibles = (
        Usuario.query
        .filter(
            Usuario.activo.is_(True),
            Usuario.rol != "admin_global"
        )
        .order_by(Usuario.nombre.asc())
        .all()
    )

    # Se pueden mostrar también miembros actuales para permitir reactivarlos.
    for usuario in usuarios_disponibles:
        usuario.ya_miembro = usuario.id in ids

    return render_template(
        "admin/grupo_miembros.html",
        grupo=grupo,
        miembros=miembros,
        usuarios_disponibles=usuarios_disponibles
    )


@admin_bp.route(
    "/grupos/<int:grupo_id>/miembros/agregar",
    methods=["POST"]
)
def agregar_miembro_global(grupo_id):
    ok, mensaje, _ = agregar_miembro_service(
        grupo_id,
        request.form.get("usuario_id", type=int),
        request.form.get("rol", "colaborador")
    )

    flash(
        mensaje,
        "success" if ok else "danger"
    )

    return redirect(
        url_for(
            "admin.grupo_miembros",
            grupo_id=grupo_id
        )
    )


@admin_bp.route(
    "/grupos/<int:grupo_id>/miembros/<int:usuario_id>/rol",
    methods=["POST"]
)
def cambiar_rol_miembro_global(grupo_id, usuario_id):
    rol = request.form.get("rol", "colaborador")

    ok, mensaje = cambiar_rol_miembro(
        grupo_id,
        usuario_id,
        rol
    )

    flash(
        mensaje,
        "success" if ok else "danger"
    )

    return redirect(
        url_for(
            "admin.grupo_miembros",
            grupo_id=grupo_id
        )
    )


@admin_bp.route(
    "/grupos/<int:grupo_id>/miembros/<int:usuario_id>/eliminar",
    methods=["POST"]
)
def eliminar_miembro(grupo_id, usuario_id):
    ok, mensaje = quitar_miembro(
        grupo_id,
        usuario_id
    )

    flash(
        mensaje,
        "success" if ok else "danger"
    )

    return redirect(
        url_for(
            "admin.grupo_miembros",
            grupo_id=grupo_id
        )
    )
