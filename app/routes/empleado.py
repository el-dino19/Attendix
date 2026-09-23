from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    flash,
    abort,
    request
)

from app.services.horas_extras import (
    obtener_hora_extra_abierta,
    iniciar_hora_extra,
    finalizar_hora_extra
)
from app.services.historial import obtener_historial_usuario
from app.services.asistencia import (
    obtener_jornada_abierta,
    registrar_salida
)
from app.services.descansos import (
    iniciar_descanso,
    finalizar_descanso,
    obtener_descanso_activo
)


empleado_bp = Blueprint(
    "empleado",
    __name__,
    url_prefix="/Attendix"
)


@empleado_bp.before_request
def proteger_empleado():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("rol") != "empleado":
        abort(403)

    if not session.get("grupo_id"):
        return redirect(url_for("grupos.seleccionar"))


@empleado_bp.route("/dashboard")
def dashboard():
    usuario_id = session["usuario_id"]
    grupo_id = session["grupo_id"]

    jornada = obtener_jornada_abierta(
        usuario_id,
        grupo_id
    )

    descanso_activo = None
    if jornada:
        descanso_activo = obtener_descanso_activo(jornada.id)

    hora_extra = obtener_hora_extra_abierta(
        usuario_id,
        grupo_id
    )

    direccion_corta = None

    if jornada and jornada.direccion:
        direccion_corta = jornada.direccion
    elif hora_extra and hora_extra.direccion:
        direccion_corta = hora_extra.direccion

    return render_template(
        "empleado/dashboard.html",
        jornada=jornada,
        descanso_activo=descanso_activo,
        hora_extra=hora_extra,
        direccion_corta=direccion_corta
    )


@empleado_bp.route("/salida", methods=["POST"])
def salida():
    jornada = registrar_salida(
        session["usuario_id"],
        session.get("zona_horaria", "UTC"),
        session["grupo_id"]
    )

    if jornada is None:
        flash("No tienes una jornada abierta.", "error")
        return redirect(url_for("empleado.dashboard"))

    flash("Jornada finalizada correctamente.", "success")
    return redirect(url_for("empleado.dashboard"))


@empleado_bp.route("/descanso/<tipo>/iniciar", methods=["POST"])
def iniciar_descanso_ruta(tipo):
    exitoso, mensaje, _ = iniciar_descanso(
        session["usuario_id"],
        tipo,
        session["grupo_id"]
    )

    flash(
        mensaje,
        "success" if exitoso else "error"
    )

    return redirect(url_for("empleado.dashboard"))


@empleado_bp.route("/descanso/finalizar", methods=["POST"])
def finalizar_descanso_ruta():
    exitoso, mensaje, _ = finalizar_descanso(
        session["usuario_id"],
        session["grupo_id"]
    )

    flash(
        mensaje,
        "success" if exitoso else "error"
    )

    return redirect(url_for("empleado.dashboard"))


@empleado_bp.route("/historial")
def historial():
    historial = obtener_historial_usuario(
        session["usuario_id"],
        session["grupo_id"]
    )

    return render_template(
        "empleado/historial.html",
        historial=historial
    )


@empleado_bp.route("/hora-extra/iniciar", methods=["POST"])
def iniciar_hora_extra_ruta():
    usuario_id = session["usuario_id"]

    latitud = request.form.get("latitud")
    longitud = request.form.get("longitud")
    direccion = request.form.get("direccion")

    try:
        latitud = float(latitud) if latitud else None
    except (TypeError, ValueError):
        latitud = None

    try:
        longitud = float(longitud) if longitud else None
    except (TypeError, ValueError):
        longitud = None

    hora_extra, mensaje = iniciar_hora_extra(
        usuario_id=usuario_id,
        zona_horaria=session.get("zona_horaria", "UTC"),
        latitud=latitud,
        longitud=longitud,
        direccion=direccion,
        grupo_id=session["grupo_id"]
    )

    flash(
        mensaje,
        "success" if hora_extra else "error"
    )

    return redirect(url_for("empleado.dashboard"))


@empleado_bp.route("/hora-extra/finalizar", methods=["POST"])
def finalizar_hora_extra_ruta():
    hora_extra, mensaje = finalizar_hora_extra(
        session["usuario_id"],
        session.get("zona_horaria", "UTC"),
        session["grupo_id"]
    )

    flash(
        mensaje,
        "success" if hora_extra else "error"
    )

    return redirect(url_for("empleado.dashboard"))
