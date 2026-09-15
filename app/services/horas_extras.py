from datetime import datetime

from app.extensions import db
from app.models.jornada import Jornada
from app.models.hora_extra import HoraExtra


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


def iniciar_hora_extra(
    usuario_id,
    latitud,
    longitud,
    ubicacion=None
):

    # Buscar jornada del usuario
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
        return False, "No tienes una jornada registrada.", None

    # Debe haber terminado la jornada
    if jornada.salida is None:
        return (
            False,
            "Debes finalizar tu jornada antes de iniciar horas extras.",
            None
        )

    # No permitir dos horas extras activas
    activa = obtener_hora_extra_activa(usuario_id)

    if activa:
        return (
            False,
            "Ya tienes unas horas extras en progreso.",
            activa
        )

    ahora = datetime.now()

    hora_extra = HoraExtra(
        jornada_id=jornada.id,
        usuario_id=usuario_id,
        inicio=ahora,
        latitud_inicio=latitud,
        longitud_inicio=longitud,
        ubicacion_inicio=ubicacion,
        estado="activa"
    )

    db.session.add(hora_extra)
    db.session.commit()

    return (
        True,
        "Horas extras iniciadas correctamente.",
        hora_extra
    )


def finalizar_hora_extra(
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

    ahora = datetime.now()

    hora_extra.fin = ahora

    hora_extra.latitud_fin = latitud
    hora_extra.longitud_fin = longitud
    hora_extra.ubicacion_fin = ubicacion

    diferencia = ahora - hora_extra.inicio

    minutos = int(
        diferencia.total_seconds() / 60
    )

    hora_extra.minutos_totales = minutos

    hora_extra.estado = "finalizada"

    db.session.commit()

    return (
        True,
        "Horas extras finalizadas correctamente.",
        hora_extra
    )
