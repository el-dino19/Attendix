from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    flash,
    abort,
    request,
    jsonify
)


# =========================================================
# SERVICIOS
# =========================================================

from app.services.horas_extras import (
    obtener_hora_extra_activa,
    iniciar_horas_extras,
    finalizar_horas_extras
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


# =========================================================
# BLUEPRINT
# =========================================================

empleado_bp = Blueprint(
    "empleado",
    __name__,
    url_prefix="/Attendix"
)


# =========================================================
# PROTECCIÓN DE TODAS LAS RUTAS DE EMPLEADO
# =========================================================

@empleado_bp.before_request
def proteger_empleado():

    # -----------------------------------------------------
    # VERIFICAR SESIÓN
    # -----------------------------------------------------

    if "usuario_id" not in session:

        return redirect(
            url_for("auth.login")
        )


    # -----------------------------------------------------
    # VERIFICAR ROL
    # -----------------------------------------------------

    if session.get("rol") != "empleado":

        abort(403)


# =========================================================
# DASHBOARD
# =========================================================

@empleado_bp.route("/dashboard")
def dashboard():

    usuario_id = session["usuario_id"]


    # -----------------------------------------------------
    # OBTENER JORNADA ABIERTA
    # -----------------------------------------------------

    jornada = obtener_jornada_abierta(
        usuario_id
    )


    # -----------------------------------------------------
    # DESCANSO ACTIVO
    # -----------------------------------------------------

    descanso_activo = None


    if jornada:

        descanso_activo = obtener_descanso_activo(
            jornada.id
        )


    # -----------------------------------------------------
    # HORAS EXTRAS ACTIVAS
    # -----------------------------------------------------

    hora_extra_activa = obtener_hora_extra_activa(
        usuario_id
    )


    # -----------------------------------------------------
    # RENDER
    # -----------------------------------------------------

    return render_template(
        "empleado/dashboard.html",

        jornada=jornada,

        descanso_activo=descanso_activo,

        hora_extra_activa=hora_extra_activa
    )


# =========================================================
# FINALIZAR JORNADA
# =========================================================

@empleado_bp.route(
    "/salida",
    methods=["POST"]
)
def salida():

    usuario_id = session["usuario_id"]


    # -----------------------------------------------------
    # VERIFICAR HORAS EXTRAS ACTIVAS
    # -----------------------------------------------------

    hora_extra_activa = obtener_hora_extra_activa(
        usuario_id
    )


    if hora_extra_activa:

        flash(
            "Debes finalizar las horas extras antes de realizar otra acción.",
            "error"
        )

        return redirect(
            url_for("empleado.dashboard")
        )


    # -----------------------------------------------------
    # OBTENER JORNADA ABIERTA
    # -----------------------------------------------------

    jornada = obtener_jornada_abierta(
        usuario_id
    )


    if jornada is None:

        flash(
            "No tienes una jornada activa.",
            "error"
        )

        return redirect(
            url_for("empleado.dashboard")
        )


    # -----------------------------------------------------
    # VERIFICAR DESCANSO ACTIVO
    # -----------------------------------------------------

    descanso_activo = obtener_descanso_activo(
        jornada.id
    )


    if descanso_activo:

        flash(
            "Debes finalizar tu descanso antes de terminar la jornada.",
            "error"
        )

        return redirect(
            url_for("empleado.dashboard")
        )


    # -----------------------------------------------------
    # REGISTRAR SALIDA
    # -----------------------------------------------------

    jornada = registrar_salida(
        usuario_id
    )


    if jornada is None:

        flash(
            "No fue posible finalizar la jornada.",
            "error"
        )

        return redirect(
            url_for("empleado.dashboard")
        )


    # -----------------------------------------------------
    # MENSAJE
    # -----------------------------------------------------

    flash(
        "Jornada finalizada correctamente. Ahora puedes iniciar horas extras.",
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

    usuario_id = session["usuario_id"]


    # -----------------------------------------------------
    # VALIDAR TIPO
    # -----------------------------------------------------

    tipos_validos = [
        "break_manana",
        "lunch",
        "break_tarde"
    ]


    if tipo not in tipos_validos:

        flash(
            "Tipo de descanso no válido.",
            "error"
        )

        return redirect(
            url_for("empleado.dashboard")
        )


    # -----------------------------------------------------
    # INICIAR DESCANSO
    # -----------------------------------------------------

    exitoso, mensaje, descanso = iniciar_descanso(
        usuario_id,
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

    usuario_id = session["usuario_id"]


    # -----------------------------------------------------
    # FINALIZAR
    # -----------------------------------------------------

    exitoso, mensaje, descanso = finalizar_descanso(
        usuario_id
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
# INICIAR HORAS EXTRAS
# =========================================================

@empleado_bp.route(
    "/horas-extras/iniciar",
    methods=["POST"]
)
def iniciar_horas_extras():

    usuario_id = session["usuario_id"]


    # -----------------------------------------------------
    # OBTENER DATOS
    # -----------------------------------------------------

    datos = request.get_json(
        silent=True
    ) or {}


    latitud = datos.get(
        "latitud"
    )


    longitud = datos.get(
        "longitud"
    )


    ubicacion = datos.get(
        "ubicacion"
    )


    # -----------------------------------------------------
    # VALIDAR GPS
    # -----------------------------------------------------

    if latitud is None or longitud is None:

        return jsonify({

            "ok": False,

            "mensaje":
                "No se pudo obtener tu ubicación. "
                "Debes permitir el acceso a la ubicación."
        }), 400


    # -----------------------------------------------------
    # CONVERTIR COORDENADAS
    # -----------------------------------------------------

    try:

        latitud = float(
            latitud
        )

        longitud = float(
            longitud
        )

    except (
        TypeError,
        ValueError
    ):

        return jsonify({

            "ok": False,

            "mensaje":
                "Las coordenadas de ubicación no son válidas."
        }), 400


    # -----------------------------------------------------
    # VALIDAR RANGO DE LATITUD
    # -----------------------------------------------------

    if not -90 <= latitud <= 90:

        return jsonify({

            "ok": False,

            "mensaje":
                "La latitud recibida no es válida."
        }), 400


    # -----------------------------------------------------
    # VALIDAR RANGO DE LONGITUD
    # -----------------------------------------------------

    if not -180 <= longitud <= 180:

        return jsonify({

            "ok": False,

            "mensaje":
                "La longitud recibida no es válida."
        }), 400


    # -----------------------------------------------------
    # VERIFICAR SI YA HAY HORAS EXTRAS ACTIVAS
    # -----------------------------------------------------

    hora_extra_existente = obtener_hora_extra_activa(
        usuario_id
    )


    if hora_extra_existente:

        return jsonify({

            "ok": False,

            "mensaje":
                "Ya tienes unas horas extras activas."
        }), 400


    from app.models.jornada import Jornada


    jornada = (
        Jornada.query
        .filter(
            Jornada.usuario_id == usuario_id
        )
        .order_by(
            Jornada.id.desc()
        )
        .first()
    )


    if jornada is None:

        return jsonify({

            "ok": False,

            "mensaje":
                "No tienes una jornada registrada."
        }), 400


    # -----------------------------------------------------
    # LA JORNADA DEBE ESTAR FINALIZADA
    # -----------------------------------------------------

    if jornada.salida is None:

        return jsonify({

            "ok": False,

            "mensaje":
                "Primero debes finalizar tu jornada antes de iniciar horas extras."
        }), 400


    # -----------------------------------------------------
    # INICIAR HORAS EXTRAS
    # -----------------------------------------------------

    exitoso, mensaje, hora_extra = iniciar_horas_extras(

        usuario_id,

        latitud,

        longitud,

        ubicacion
    )


    if not exitoso:

        return jsonify({

            "ok": False,

            "mensaje": mensaje
        }), 400


    # -----------------------------------------------------
    # RESPUESTA
    # -----------------------------------------------------

    return jsonify({

        "ok": True,

        "mensaje": mensaje,

        "hora_extra_id":
            hora_extra.id,

        "inicio":
            hora_extra.inicio.isoformat()
    })


# =========================================================
# FINALIZAR HORAS EXTRAS
# =========================================================

@empleado_bp.route(
    "/horas-extras/finalizar",
    methods=["POST"]
)
def finalizar_horas_extras_ruta():

    usuario_id = session["usuario_id"]


    # -----------------------------------------------------
    # OBTENER DATOS
    # -----------------------------------------------------

    datos = request.get_json(
        silent=True
    ) or {}


    latitud = datos.get(
        "latitud"
    )


    longitud = datos.get(
        "longitud"
    )


    ubicacion = datos.get(
        "ubicacion"
    )


    # -----------------------------------------------------
    # VALIDAR GPS
    # -----------------------------------------------------

    if latitud is None or longitud is None:

        return jsonify({

            "ok": False,

            "mensaje":
                "No se pudo obtener tu ubicación para finalizar las horas extras."
        }), 400


    # -----------------------------------------------------
    # CONVERTIR COORDENADAS
    # -----------------------------------------------------

    try:

        latitud = float(
            latitud
        )

        longitud = float(
            longitud
        )

    except (
        TypeError,
        ValueError
    ):

        return jsonify({

            "ok": False,

            "mensaje":
                "Las coordenadas de ubicación no son válidas."
        }), 400


    # -----------------------------------------------------
    # VALIDAR RANGO
    # -----------------------------------------------------

    if not -90 <= latitud <= 90:

        return jsonify({

            "ok": False,

            "mensaje":
                "La latitud recibida no es válida."
        }), 400


    if not -180 <= longitud <= 180:

        return jsonify({

            "ok": False,

            "mensaje":
                "La longitud recibida no es válida."
        }), 400


    # -----------------------------------------------------
    # VERIFICAR HORA EXTRA ACTIVA
    # -----------------------------------------------------

    hora_extra_activa = obtener_hora_extra_activa(
        usuario_id
    )


    if hora_extra_activa is None:

        return jsonify({

            "ok": False,

            "mensaje":
                "No tienes horas extras activas."
        }), 400


    # -----------------------------------------------------
    # FINALIZAR HORAS EXTRAS
    # -----------------------------------------------------

    exitoso, mensaje, hora_extra = finalizar_horas_extras(

        usuario_id,

        latitud,

        longitud,

        ubicacion
    )


    if not exitoso:

        return jsonify({

            "ok": False,

            "mensaje": mensaje
        }), 400


    # -----------------------------------------------------
    # RESPUESTA
    # -----------------------------------------------------

    return jsonify({

        "ok": True,

        "mensaje": mensaje,

        "minutos_totales":
            hora_extra.minutos_totales,

        "inicio":
            hora_extra.inicio.isoformat(),

        "fin":
            hora_extra.fin.isoformat()
    })


# =========================================================
# ESTADO DE HORAS EXTRAS
# =========================================================

@empleado_bp.route(
    "/horas-extras/estado",
    methods=["GET"]
)
def estado_horas_extras():

    usuario_id = session["usuario_id"]


    # -----------------------------------------------------
    # OBTENER ACTIVA
    # -----------------------------------------------------

    hora_extra = obtener_hora_extra_activa(
        usuario_id
    )


    # -----------------------------------------------------
    # NO EXISTE
    # -----------------------------------------------------

    if hora_extra is None:

        return jsonify({

            "ok": True,

            "activa": False
        })


    # -----------------------------------------------------
    # EXISTE
    # -----------------------------------------------------

    return jsonify({

        "ok": True,

        "activa": True,

        "id":
            hora_extra.id,

        "inicio":
            hora_extra.inicio.isoformat(),

        "ubicacion_inicio":
            hora_extra.ubicacion_inicio
    })


# =========================================================
# HISTORIAL
# =========================================================

@empleado_bp.route(
    "/historial"
)
def historial():

    historial = obtener_historial_usuario(
        session["usuario_id"]
    )


    return render_template(
        "empleado/historial.html",

        historial=historial
    )
