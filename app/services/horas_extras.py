from datetime import datetime
from zoneinfo import ZoneInfo

from app.extensions import db
from app.models.hora_extra import HoraExtra


def obtener_hora_actual(zona_horaria="UTC"):

    try:
        zona = ZoneInfo(zona_horaria)
    except Exception:
        zona = ZoneInfo("UTC")

    return datetime.now(zona).time()


def obtener_fecha_actual(zona_horaria="UTC"):

    try:
        zona = ZoneInfo(zona_horaria)
    except Exception:
        zona = ZoneInfo("UTC")

    return datetime.now(zona).date()


def obtener_hora_extra_abierta(usuario_id):

    return HoraExtra.query.filter(
        HoraExtra.usuario_id == usuario_id,
        HoraExtra.fin.is_(None)
    ).order_by(
        HoraExtra.inicio.desc()
    ).first()


def iniciar_hora_extra(
    usuario_id,
    zona_horaria="UTC",
    latitud=None,
    longitud=None,
    direccion=None
):

    hora_extra_abierta = obtener_hora_extra_abierta(
        usuario_id
    )

    if hora_extra_abierta:

        return (
            None,
            "Ya tienes una hora extra activa."
        )

    hora_extra = HoraExtra(
        usuario_id=usuario_id,
        fecha=obtener_fecha_actual(zona_horaria),
        inicio=obtener_hora_actual(zona_horaria),
        latitud=latitud,
        longitud=longitud,
        direccion=direccion
    )

    db.session.add(hora_extra)
    db.session.commit()

    return (
        hora_extra,
        "Hora extra iniciada correctamente."
    )


def finalizar_hora_extra(
    usuario_id,
    zona_horaria="UTC"
):

    hora_extra = obtener_hora_extra_abierta(
        usuario_id
    )

    if hora_extra is None:

        return (
            None,
            "No tienes una hora extra activa."
        )

    hora_extra.fin = obtener_hora_actual(
        zona_horaria
    )

    db.session.commit()

    return (
        hora_extra,
        "Hora extra finalizada correctamente."
    )
