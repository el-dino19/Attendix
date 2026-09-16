from datetime import datetime
from zoneinfo import ZoneInfo

from app import db
from app.models.jornada import Jornada


def obtener_hora_actual(zona_horaria="UTC"):

    try:
        zona = ZoneInfo(zona_horaria)
    except Exception:
        zona = ZoneInfo("UTC")

    ahora = datetime.now(zona)

    return ahora.time()


def obtener_fecha_actual(zona_horaria="UTC"):

    try:
        zona = ZoneInfo(zona_horaria)
    except Exception:
        zona = ZoneInfo("UTC")

    ahora = datetime.now(zona)

    return ahora.date()


def obtener_jornada_abierta(usuario_id):

    jornada = Jornada.query.filter(
        Jornada.usuario_id == usuario_id,
        Jornada.salida.is_(None)
    ).order_by(
        Jornada.entrada.desc()
    ).first()

    return jornada


def registrar_entrada(
    usuario_id,
    zona_horaria="UTC",
    latitud=None,
    longitud=None,
    direccion=None
):

    try:
        zona = ZoneInfo(zona_horaria)
    except Exception:
        zona = ZoneInfo("UTC")

    ahora = datetime.now(zona)

    fecha_hoy = ahora.date()
    hora_actual = ahora.time()

    jornada_existente = Jornada.query.filter(
        Jornada.usuario_id == usuario_id,
        Jornada.fecha == fecha_hoy
    ).first()

    if jornada_existente:
        return jornada_existente

    jornada = Jornada(
        usuario_id=usuario_id,
        fecha=fecha_hoy,
        entrada=hora_actual,
        latitud=latitud,
        longitud=longitud,
        direccion=direccion
    )

    db.session.add(jornada)
    db.session.commit()

    return jornada




def registrar_salida(usuario_id, zona_horaria="UTC"):

    jornada = obtener_jornada_abierta(
        usuario_id
    )

    if jornada is None:
        return None

    jornada.salida = obtener_hora_actual(
        zona_horaria
    )

    db.session.commit()

    return jornada
