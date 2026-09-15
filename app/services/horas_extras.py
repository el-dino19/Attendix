
from datetime import datetime, timezone

from app.extensions import db
from app.models.hora_extra import HoraExtra
from app.models.jornada import Jornada


# OBTENER UTC ACTUAL
def obtener_utc_actual():
    return datetime.now(timezone.utc)


# ASEGURAR UTC
def asegurar_utc(fecha):
    if fecha is None:
        return None

    if fecha.tzinfo is None:
        return fecha.replace(tzinfo=timezone.utc)

    return fecha.astimezone(timezone.utc)


# OBTENER HORA EXTRA ACTIVA
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


# INICIAR HORAS EXTRAS
def iniciar_horas_extras(
    usuario_id,
    latitud,
    longitud,
    ubicacion=None
):
    hora_extra_existente = obtener_hora_extra_activa(
        usuario_id
    )

    if hora_extra_existente:
        return (
            False,
            "Ya tienes unas horas extras activas.",
            hora_extra_existente
        )

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

    if jornada.salida is None:
        return (
            False,
            "Debes finalizar tu jornada antes de iniciar horas extras.",
            None
        )

    hora_extra = HoraExtra(
        jornada_id=jornada.id,
        usuario_id=usuario_id,
        inicio=obtener_utc_actual(),
        fin=None,
        latitud_inicio=latitud,
        longitud_inicio=longitud,
        ubicacion_inicio=ubicacion,
        estado="activa"
    )

    try:
        db.session.add(hora_extra)
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


# FINALIZAR HORAS EXTRAS
def finalizar_horas_extras(
    usuario_id,
    latitud=None,
    longitud=None,
    ubicacion=None
):
    hora_extra = obtener_hora_extra_activa(
        usuario_id
    )

    if hora_extra is None:
        return (
            False,
            "No tienes horas extras activas.",
            None
        )

    inicio = asegurar_utc(
        hora_extra.inicio
    )

    fin = obtener_utc_actual()

    hora_extra.fin = fin

    hora_extra.latitud_fin = latitud
    hora_extra.longitud_fin = longitud
    hora_extra.ubicacion_fin = ubicacion

    diferencia = fin - inicio

    hora_extra.minutos_totales = int(
        diferencia.total_seconds() / 60
    )

    if hora_extra.minutos_totales < 0:
        hora_extra.minutos_totales = 0

    hora_extra.estado = "finalizada"

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

