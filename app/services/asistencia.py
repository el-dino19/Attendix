from datetime import datetime
from zoneinfo import ZoneInfo

from app.extensions import db
from app.models.jornada import Jornada


# =========================================================
# ZONA HORARIA
# =========================================================

ZONA_HORARIA = ZoneInfo("America/Bogota")


# =========================================================
# HORA ACTUAL
# =========================================================

def obtener_hora_actual():

    ahora = datetime.now(
        ZONA_HORARIA
    )

    return ahora.time()


# =========================================================
# FECHA ACTUAL
# =========================================================

def obtener_fecha_actual():

    ahora = datetime.now(
        ZONA_HORARIA
    )

    return ahora.date()


# =========================================================
# OBTENER JORNADA ABIERTA
# =========================================================

def obtener_jornada_abierta(usuario_id):

    jornada = (
        Jornada.query
        .filter(
            Jornada.usuario_id == usuario_id,
            Jornada.salida.is_(None)
        )
        .order_by(
            Jornada.fecha.desc(),
            Jornada.entrada.desc()
        )
        .first()
    )

    return jornada


# =========================================================
# REGISTRAR ENTRADA
# =========================================================

def registrar_entrada(usuario_id):

    ahora = datetime.now(
        ZONA_HORARIA
    )

    fecha_hoy = ahora.date()
    hora_actual = ahora.time()


    # =====================================================
    # BUSCAR JORNADA DEL DÍA
    # =====================================================

    jornada_existente = (
        Jornada.query
        .filter(
            Jornada.usuario_id == usuario_id,
            Jornada.fecha == fecha_hoy
        )
        .first()
    )


    # =====================================================
    # SI YA EXISTE
    # =====================================================

    if jornada_existente:

        return jornada_existente


    # =====================================================
    # CREAR JORNADA
    # =====================================================

    jornada = Jornada(

        usuario_id=usuario_id,

        fecha=fecha_hoy,

        entrada=hora_actual,

        salida=None

    )


    try:

        db.session.add(
            jornada
        )

        db.session.commit()

        return jornada


    except Exception as e:

        db.session.rollback()

        print(
            "ERROR registrando entrada:"
        )

        print(
            type(e).__name__,
            str(e)
        )

        # -------------------------------------------------
        # IMPORTANTE
        # -------------------------------------------------
        # No dejamos que un problema al registrar
        # la asistencia destruya el login.
        #
        # Devolvemos None para que el usuario pueda
        # iniciar sesión.

        return None


# =========================================================
# REGISTRAR SALIDA
# =========================================================

def registrar_salida(usuario_id):

    jornada = obtener_jornada_abierta(
        usuario_id
    )


    if jornada is None:

        return None


    # =====================================================
    # REGISTRAR HORA DE SALIDA
    # =====================================================

    jornada.salida = obtener_hora_actual()


    try:

        db.session.commit()

        return jornada


    except Exception as e:

        db.session.rollback()

        print(
            "ERROR registrando salida:"
        )

        print(
            type(e).__name__,
            str(e)
        )

        return None
