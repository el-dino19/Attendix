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

from app.services.exportacion import generar_excel_asistencia
from app.models.usuario import Usuario
from app.models.jornada import Jornada

from app.services.usuarios_admin import (
    obtener_usuarios,
    crear_usuario,
    editar_usuario,
    cambiar_password,
    cambiar_estado_usuario
)


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/Attendix"
)


# =========================================================
# PROTECCION DE TODAS LAS RUTAS ADMIN
# =========================================================

@admin_bp.before_request
def proteger_admin():

    # ==========================================
    # VERIFICAR QUE HAYA INICIADO SESION
    # ==========================================

    if "usuario_id" not in session:

        return redirect(
            url_for("auth.login")
        )


    # ==========================================
    # VERIFICAR QUE SEA ADMIN
    # ==========================================

    if session.get("rol") != "admin":

        abort(403)


# =========================================================
# DASHBOARD ADMIN
# =========================================================

@admin_bp.route("/")
def dashboard():

    cantidad_usuarios = Usuario.query.count()

    usuarios_activos = Usuario.query.filter_by(
        activo=True
    ).count()

    usuarios_inactivos = Usuario.query.filter_by(
        activo=False
    ).count()

    return render_template(
        "admin/dashboard.html",
        cantidad_usuarios=cantidad_usuarios,
        usuarios_activos=usuarios_activos,
        usuarios_inactivos=usuarios_inactivos
    )


# =========================================================
# LISTAR USUARIOS
# =========================================================

@admin_bp.route("/usuarios")
def usuarios():

    usuarios = obtener_usuarios()

    return render_template(
        "admin/usuarios.html",
        usuarios=usuarios
    )


# =========================================================
# CREAR USUARIO
# =========================================================

@admin_bp.route(
    "/usuarios/crear",
    methods=["POST"]
)
def crear():

    nombre = request.form.get(
        "nombre",
        ""
    ).strip()

    correo = request.form.get(
        "correo",
        ""
    ).strip().lower()

    password = request.form.get(
        "password",
        ""
    )

    rol = request.form.get(
        "rol",
        "empleado"
    )


    # ==========================================
    # VALIDAR CORREO DUPLICADO
    # ==========================================

    usuario_existente = Usuario.query.filter_by(
        correo=correo
    ).first()

    if usuario_existente:

        flash(
            "Ya existe un usuario registrado con ese correo.",
            "danger"
        )

        return redirect(
            url_for("admin.usuarios")
        )


    if not nombre:

        flash(
            "El nombre es obligatorio.",
            "danger"
        )

        return redirect(
            url_for("admin.usuarios")
        )


    if not correo:

        flash(
            "El correo es obligatorio.",
            "danger"
        )

        return redirect(
            url_for("admin.usuarios")
        )


    if not password:

        flash(
            "La contraseña es obligatoria.",
            "danger"
        )

        return redirect(
            url_for("admin.usuarios")
        )


    exito, mensaje, usuario = crear_usuario(
        nombre,
        correo,
        password,
        rol
    )


    if exito:

        flash(
            mensaje,
            "success"
        )

    else:

        flash(
            mensaje,
            "danger"
        )


    return redirect(
        url_for("admin.usuarios")
    )


# =========================================================
# EDITAR USUARIO
# =========================================================

@admin_bp.route(
    "/usuarios/<int:usuario_id>/editar",
    methods=["POST"]
)
def editar(usuario_id):

    nombre = request.form.get(
        "nombre",
        ""
    ).strip()

    correo = request.form.get(
        "correo",
        ""
    ).strip().lower()

    rol = request.form.get(
        "rol",
        "empleado"
    )


    if not nombre or not correo:

        flash(
            "Nombre y correo son obligatorios.",
            "danger"
        )

        return redirect(
            url_for("admin.usuarios")
        )


    exito, mensaje, usuario = editar_usuario(
        usuario_id,
        nombre,
        correo,
        rol
    )


    if exito:

        flash(
            mensaje,
            "success"
        )

    else:

        flash(
            mensaje,
            "danger"
        )


    return redirect(
        url_for("admin.usuarios")
    )


# =========================================================
# CAMBIAR CONTRASEÑA
# =========================================================

@admin_bp.route(
    "/usuarios/<int:usuario_id>/password",
    methods=["POST"]
)
def cambiar_password_ruta(usuario_id):

    password = request.form.get(
        "password",
        ""
    )


    if not password:

        flash(
            "La contraseña no puede estar vacía.",
            "danger"
        )

        return redirect(
            url_for("admin.usuarios")
        )


    exito, mensaje = cambiar_password(
        usuario_id,
        password
    )


    if exito:

        flash(
            mensaje,
            "success"
        )

    else:

        flash(
            mensaje,
            "danger"
        )


    return redirect(
        url_for("admin.usuarios")
    )


# =========================================================
# ACTIVAR / DESACTIVAR
# =========================================================

@admin_bp.route(
    "/usuarios/<int:usuario_id>/estado",
    methods=["POST"]
)
def cambiar_estado(usuario_id):

    # El admin no puede desactivarse a sí mismo

    if usuario_id == session.get("usuario_id"):

        flash(
            "No puedes desactivar tu propio usuario.",
            "danger"
        )

        return redirect(
            url_for("admin.usuarios")
        )


    exito, mensaje = cambiar_estado_usuario(
        usuario_id
    )


    if exito:

        flash(
            mensaje,
            "success"
        )

    else:

        flash(
            mensaje,
            "danger"
        )


    return redirect(
        url_for("admin.usuarios")
    )




# =========================================================
# EXPORTAR ASISTENCIA A EXCEL
# =========================================================

@admin_bp.route("/exportar")
def exportar():

    # ==========================================
    # OBTENER PARÁMETROS DEL FORMULARIO
    # ==========================================

    periodo = request.args.get(
        "periodo",
        "todos"
    )

    mes = request.args.get(
        "mes",
        ""
    ).strip()


    # ==========================================
    # OBTENER REGISTROS
    # ==========================================

    registros = (
        Jornada.query
        .join(Usuario)
        .filter(
            Usuario.rol != "admin"
        )
        .order_by(
            Jornada.fecha.desc(),
            Jornada.entrada.desc()
        )
        .all()
    )


    # ==========================================
    # GENERAR EXCEL
    # ==========================================

    archivo = generar_excel_asistencia(
        registros,
        periodo=periodo,
        mes=mes
    )


    # ==========================================
    # HORA LOCAL DE BOGOTÁ
    # ==========================================

    ahora = datetime.now(
        ZoneInfo("America/Bogota")
    )


    # ==========================================
    # NOMBRE DEL ARCHIVO
    # ==========================================

    if periodo == "mes" and mes:

        nombre_archivo = (
            f"Reporte_Asistencia_"
            f"{mes}.xlsx"
        )

    elif periodo == "3_meses":

        nombre_archivo = (
            "Reporte_Asistencia_"
            "Ultimos_3_Meses.xlsx"
        )

    elif periodo == "6_meses":

        nombre_archivo = (
            "Reporte_Asistencia_"
            "Ultimos_6_Meses.xlsx"
        )

    else:

        nombre_archivo = (
            f"Reporte_Asistencia_"
            f"{ahora.strftime('%Y-%m-%d')}"
            f".xlsx"
        )


    # ==========================================
    # DESCARGAR
    # ==========================================

    return send_file(
        archivo,
        as_attachment=True,
        download_name=nombre_archivo,
        mimetype=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )


# =========================================================
# VISTA DE ASISTENCIA
# =========================================================

@admin_bp.route("/asistencia")
def asistencia():

    usuario_id = request.args.get("usuario_id")
    fecha_desde = request.args.get("fecha_desde")
    fecha_hasta = request.args.get("fecha_hasta")

    # ==========================================
    # CONSULTA DE JORNADAS
    # Solo colaboradores, nunca administradores
    # ==========================================

    query = (
        Jornada.query
        .join(Usuario)
        .filter(Usuario.rol != "admin")
    )

    # ==========================================
    # FILTRO POR COLABORADOR
    # ==========================================

    if usuario_id:
        query = query.filter(
            Jornada.usuario_id == int(usuario_id)
        )

    # ==========================================
    # FILTRO FECHA DESDE
    # ==========================================

    if fecha_desde:
        query = query.filter(
            Jornada.fecha >= fecha_desde
        )

    # ==========================================
    # FILTRO FECHA HASTA
    # ==========================================

    if fecha_hasta:
        query = query.filter(
            Jornada.fecha <= fecha_hasta
        )

    # ==========================================
    # ORDEN
    # ==========================================

    jornadas = query.order_by(
        Jornada.fecha.desc(),
        Jornada.entrada.desc()
    ).all()

    # ==========================================
    # USUARIOS PARA EL SELECT
    # Solo colaboradores
    # ==========================================

    usuarios = (
        Usuario.query
        .filter(Usuario.rol != "admin")
        .order_by(Usuario.nombre.asc())
        .all()
    )

    # ==========================================
    # RENDER
    # ==========================================

    return render_template(
        "admin/asistencias.html",
        jornadas=jornadas,
        usuarios=usuarios
    )

