from datetime import datetime
from zoneinfo import ZoneInfo

from app.extensions import db
from app.models.hora_extra import HoraExtra
from app.models.jornada import Jornada


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


def obtener_hora_extra_abierta(usuario_id, grupo_id=None):
    query = HoraExtra.query.filter(
        HoraExtra.usuario_id == usuario_id,
        HoraExtra.fin.is_(None)
    )

    if grupo_id is not None:
        query = query.filter(HoraExtra.grupo_id == grupo_id)

    return query.order_by(
        HoraExtra.inicio.desc()
    ).first()


def obtener_hora_extra_del_dia(usuario_id, fecha, grupo_id=None):
    query = HoraExtra.query.filter(
        HoraExtra.usuario_id == usuario_id,
        HoraExtra.fecha == fecha
    )

    if grupo_id is not None:
        query = query.filter(HoraExtra.grupo_id == grupo_id)

    return query.order_by(
        HoraExtra.inicio.desc()
    ).first()


def iniciar_hora_extra(
    usuario_id,
    zona_horaria="UTC",
    latitud=None,
    longitud=None,
    direccion=None,
    grupo_id=None
):
    if grupo_id is None:
        return None, "Debes seleccionar un grupo antes de iniciar horas extras."

    fecha = obtener_fecha_actual(zona_horaria)
    hora = obtener_hora_actual(zona_horaria)

    if obtener_hora_extra_abierta(usuario_id, grupo_id):
        return None, "Ya tienes una hora extra activa."

    if obtener_hora_extra_del_dia(usuario_id, fecha, grupo_id):
        return None, "Ya registraste una hora extra el día de hoy."

    jornada = Jornada.query.filter(
        Jornada.usuario_id == usuario_id,
        Jornada.grupo_id == grupo_id,
        Jornada.fecha == fecha
    ).first()

    if jornada is None:
        return (
            None,
            "No puedes iniciar horas extras porque no tienes una jornada registrada para hoy."
        )

    hora_extra = HoraExtra(
        usuario_id=usuario_id,
        grupo_id=grupo_id,
        jornada_id=jornada.id,
        fecha=fecha,
        inicio=hora,
        latitud=latitud,
        longitud=longitud,
        direccion=(direccion.strip() if direccion else None)
    )

    db.session.add(hora_extra)
    db.session.commit()

    return hora_extra, "Hora extra iniciada correctamente."


def finalizar_hora_extra(usuario_id, zona_horaria="UTC", grupo_id=None):
    hora_extra = obtener_hora_extra_abierta(
        usuario_id,
        grupo_id
    )

    if hora_extra is None:
        return None, "No tienes una hora extra activa."

    hora_extra.fin = obtener_hora_actual(zona_horaria)
    db.session.commit()

    return hora_extra, "Hora extra finalizada correctamente."
