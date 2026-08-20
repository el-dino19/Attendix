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

    jornada_abierta = obtener_jornada_abierta(
        usuario_id
    )

    if jornada_abierta:

        return jornada_abierta, False

    jornada = Jornada(
        usuario_id=usuario_id,
        fecha=obtener_fecha_actual(),
        entrada=obtener_hora_actual()
    )

    db.session.add(jornada)

    db.session.commit()

    return jornada, True


def registrar_salida(usuario_id):

    jornada = obtener_jornada_abierta(
        usuario_id
    )

    if jornada is None:

        return None

    jornada.salida = obtener_hora_actual()

    db.session.commit()

    return jornada