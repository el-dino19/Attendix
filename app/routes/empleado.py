from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    flash,
    abort
)

from app.services.historial import (
    obtener_historial_usuario
)

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
    url_prefix="/empleado"
)


# =========================================================
# PROTECCION DE TODAS LAS RUTAS DE EMPLEADO
# =========================================================

@empleado_bp.before_request
def proteger_empleado():

    # ==========================================
    # VERIFICAR QUE HAYA INICIADO SESION
    # ==========================================

    if "usuario_id" not in session:

        return redirect(
            url_for("auth.login")
        )


    # ==========================================
    # VERIFICAR QUE SEA EMPLEADO
    # ==========================================

    if session.get("rol") != "empleado":

        abort(403)


# =========================================================
# DASHBOARD
# =========================================================

@empleado_bp.route("/dashboard")
def dashboard():

    jornada = obtener_jornada_abierta(
        session["usuario_id"]
    )


    descanso_activo = None

    if jornada:

        descanso_activo = obtener_descanso_activo(
            jornada.id
        )


    return render_template(
        "empleado/dashboard.html",
        jornada=jornada,
        descanso_activo=descanso_activo
    )


# =========================================================
# SALIDA
# =========================================================

@empleado_bp.route("/salida", methods=["POST"])
def salida():

    jornada = registrar_salida(
        session["usuario_id"]
    )


    if jornada is None:

        flash(
            "No tienes una jornada abierta.",
            "error"
        )

        return redirect(
            url_for("empleado.dashboard")
        )


    flash(
        "Jornada finalizada correctamente.",
        "success"
    )


    return redirect(
        url_for("empleado.dashboard")
    )


# =========================================================
# INICIAR DESCANSO
# =========================================================

@empleado_bp.route(
    "/descanso/<tipo>/iniciar",
    methods=["POST"]
)
def iniciar_descanso_ruta(tipo):

    exitoso, mensaje, descanso = iniciar_descanso(
        session["usuario_id"],
        tipo
    )


    if exitoso:

        flash(
            mensaje,
            "success"
        )

    else:

        flash(
            mensaje,
            "error"
        )


    return redirect(
        url_for("empleado.dashboard")
    )


# =========================================================
# FINALIZAR DESCANSO
# =========================================================

@empleado_bp.route(
    "/descanso/finalizar",
    methods=["POST"]
)
def finalizar_descanso_ruta():

    exitoso, mensaje, descanso = finalizar_descanso(
        session["usuario_id"]
    )


    if exitoso:

        flash(
            mensaje,
            "success"
        )

    else:

        flash(
            mensaje,
            "error"
        )


    return redirect(
        url_for("empleado.dashboard")
    )


# =========================================================
# HISTORIAL
# =========================================================

@empleado_bp.route("/historial")
def historial():

    historial = obtener_historial_usuario(
        session["usuario_id"]
    )


    return render_template(
        "empleado/historial.html",
        historial=historial
    )
