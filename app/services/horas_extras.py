from datetime import datetime

from app.extensions import db
from app.models.hora_extra import HoraExtra
from app.models.jornada import Jornada


# =========================================================
# OBTENER HORA EXTRA ACTIVA
# =========================================================

def obtener_hora_extra_activa(usuario_id):

    return (
        HoraExtra.query
        .filter(
            HoraExtra.usuario_id == usuario_id,
            HoraExtra.estado == "activa"
        )
        .order_by(
            HoraExtra.inicio.desc()
        )
        .first()
    )


# =========================================================
# INICIAR HORAS EXTRAS
# =========================================================

def iniciar_horas_extras(
    usuario_id,
    latitud,
    longitud,
    ubicacion=None
):

    # -----------------------------------------------------
    # VERIFICAR SI YA EXISTE UNA HORA EXTRA ACTIVA
    # -----------------------------------------------------

    hora_extra_existente = obtener_hora_extra_activa(
        usuario_id
    )

    if hora_extra_existente:

        return (
            False,
            "Ya tienes unas horas extras activas.",
            hora_extra_existente
        )


    # -----------------------------------------------------
    # BUSCAR LA ÚLTIMA JORNADA
    # -----------------------------------------------------

    jornada = (
        Jornada.query
        .filter(
            Jornada.usuario_id == usuario_id
        )
        .order_by(
            Jornada.fecha.desc(),
            Jornada.entrada.desc()
        )
        .first()
    )


    if jornada is None:

        return (
            False,
            "No tienes una jornada registrada.",
            None
        )


    # -----------------------------------------------------
    # LA JORNADA DEBE ESTAR FINALIZADA
    # -----------------------------------------------------

    if jornada.salida is None:

        return (
            False,
            "Debes finalizar tu jornada antes de iniciar horas extras.",
            None
        )


    # -----------------------------------------------------
    # CREAR HORA EXTRA
    # -----------------------------------------------------

    hora_extra = HoraExtra(

        jornada_id=jornada.id,

        usuario_id=usuario_id,

        inicio=datetime.utcnow(),

        fin=None,

        latitud_inicio=latitud,

        longitud_inicio=longitud,

        ubicacion_inicio=ubicacion,

        estado="activa"
    )


    try:

        db.session.add(
            hora_extra
        )

        db.session.commit()

        return (
            True,
            "Horas extras iniciadas correctamente.",
            hora_extra
        )

    except Exception as e:

        db.session.rollback()

        print(
            "Error iniciando horas extras:",
            e
        )

        return (
            False,
            "No se pudieron iniciar las horas extras.",
            None
        )


# =========================================================
# FINALIZAR HORAS EXTRAS
# =========================================================

def finalizar_horas_extras(
    usuario_id,
    latitud=None,
    longitud=None,
    ubicacion=None
):

    # -----------------------------------------------------
    # BUSCAR HORA EXTRA ACTIVA
    # -----------------------------------------------------

    hora_extra = obtener_hora_extra_activa(
        usuario_id
    )


    if hora_extra is None:

        return (
            False,
            "No tienes horas extras activas.",
            None
        )


    # -----------------------------------------------------
    # HORA DE FINALIZACIÓN
    # -----------------------------------------------------

    hora_extra.fin = datetime.utcnow()


    # -----------------------------------------------------
    # UBICACIÓN FINAL
    # -----------------------------------------------------

    hora_extra.latitud_fin = latitud

    hora_extra.longitud_fin = longitud

    hora_extra.ubicacion_fin = ubicacion


    # -----------------------------------------------------
    # CALCULAR MINUTOS
    # -----------------------------------------------------

    diferencia = (
        hora_extra.fin -
        hora_extra.inicio
    )


    hora_extra.minutos_totales = int(
        diferencia.total_seconds() / 60
    )


    # -----------------------------------------------------
    # CAMBIAR ESTADO
    # -----------------------------------------------------

    hora_extra.estado = "finalizada"


    # -----------------------------------------------------
    # GUARDAR
    # -----------------------------------------------------

    try:

        db.session.commit()

        return (
            True,
            "Horas extras finalizadas correctamente.",
            hora_extra
        )

    except Exception as e:

        db.session.rollback()

        print(
            "Error finalizando horas extras:",
            e
        )

        return (
            False,
            "No se pudieron finalizar las horas extras.",
            None
        )
