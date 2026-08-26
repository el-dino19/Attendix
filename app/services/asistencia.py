from datetime import datetime
from zoneinfo import ZoneInfo

from app import db
from app.models.jornada import Jornada


ZONA_HORARIA = ZoneInfo("America/Chicago")


def obtener_hora_actual():

    ahora = datetime.now(
        ZONA_HORARIA
    )

    return ahora.time()


def obtener_fecha_actual():

    ahora = datetime.now(
        ZONA_HORARIA
    )

    return ahora.date()


def obtener_jornada_abierta(usuario_id):

    jornada = Jornada.query.filter(
        Jornada.usuario_id == usuario_id,
        Jornada.salida.is_(None)
    ).order_by(
        Jornada.entrada.desc()
    ).first()

    return jornada


def registrar_entrada(usuario_id):

    ahora = datetime.now(ZONA_HORARIA)

    fecha_hoy = ahora.date()
    hora_actual = ahora.time()

    # ==========================================
    # VERIFICAR SI YA EXISTE JORNADA HOY
    # ==========================================

    jornada_existente = Jornada.query.filter(
        Jornada.usuario_id == usuario_id,
        Jornada.fecha == fecha_hoy
    ).first()

    if jornada_existente:

        return jornada_existente

    # ==========================================
    # CREAR NUEVA JORNADA
    # ==========================================

    jornada = Jornada(
        usuario_id=usuario_id,
        fecha=fecha_hoy,
        entrada=hora_actual
    )

    db.session.add(jornada)
    db.session.commit()

    return jornada


def registrar_salida(usuario_id):

    jornada = obtener_jornada_abierta(
        usuario_id
    )

    if jornada is None:

        return None

    jornada.salida = obtener_hora_actual()

    db.session.commit()

    return jornada