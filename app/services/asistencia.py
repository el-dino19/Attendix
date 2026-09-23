from datetime import datetime
from zoneinfo import ZoneInfo

from app import db
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


def formatear_direccion_corta(direccion):
    if not direccion:
        return "Ubicación no disponible"

    partes = [
        parte.strip()
        for parte in direccion.split(",")
        if parte.strip()
    ]

    resultado = []
    for parte in partes:
        if parte not in resultado:
            resultado.append(parte)

    if len(resultado) > 6:
        resultado = resultado[:6]

    return ", ".join(resultado)


def obtener_jornada_abierta(usuario_id, grupo_id=None):
    query = Jornada.query.filter(
        Jornada.usuario_id == usuario_id,
        Jornada.salida.is_(None)
    )

    if grupo_id is not None:
        query = query.filter(Jornada.grupo_id == grupo_id)

    return query.order_by(
        Jornada.fecha.desc(),
        Jornada.entrada.desc()
    ).first()


def registrar_entrada(
    usuario_id,
    zona_horaria="UTC",
    latitud=None,
    longitud=None,
    direccion=None,
    grupo_id=None
):
    if grupo_id is None:
        raise ValueError("grupo_id es obligatorio para registrar asistencia.")

    try:
        zona = ZoneInfo(zona_horaria)
    except Exception:
        zona = ZoneInfo("UTC")

    ahora = datetime.now(zona)
    fecha_hoy = ahora.date()
    hora_actual = ahora.time()

    jornada_existente = Jornada.query.filter(
        Jornada.usuario_id == usuario_id,
        Jornada.grupo_id == grupo_id,
        Jornada.fecha == fecha_hoy
    ).first()

    if jornada_existente:
        return jornada_existente

    direccion = direccion.strip() if direccion else None

    jornada = Jornada(
        usuario_id=usuario_id,
        grupo_id=grupo_id,
        fecha=fecha_hoy,
        entrada=hora_actual,
        latitud=latitud,
        longitud=longitud,
        direccion=direccion
    )

    db.session.add(jornada)
    db.session.commit()

    return jornada


def registrar_salida(usuario_id, zona_horaria="UTC", grupo_id=None):
    jornada = obtener_jornada_abierta(
        usuario_id,
        grupo_id
    )

    if jornada is None:
        return None

    jornada.salida = obtener_hora_actual(zona_horaria)
    db.session.commit()

    return jornada
