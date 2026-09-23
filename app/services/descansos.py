from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app import db
from app.models.descanso import Descanso
from app.models.jornada import Jornada


ZONA_HORARIA = ZoneInfo("America/Chicago")

TIPOS_DESCANSO = {
    "break_manana": 15,
    "lunch": 60,
    "break_tarde": 15
}


def obtener_hora_actual():
    return datetime.now(ZONA_HORARIA).time()


def obtener_jornada_abierta(usuario_id, grupo_id=None):
    query = Jornada.query.filter(
        Jornada.usuario_id == usuario_id,
        Jornada.salida.is_(None)
    )

    if grupo_id is not None:
        query = query.filter(Jornada.grupo_id == grupo_id)

    return query.order_by(
        Jornada.entrada.desc()
    ).first()


def obtener_descanso_activo(jornada_id):
    return Descanso.query.filter(
        Descanso.jornada_id == jornada_id,
        Descanso.fin.is_(None)
    ).first()


def obtener_descanso_tipo(jornada_id, tipo):
    return Descanso.query.filter(
        Descanso.jornada_id == jornada_id,
        Descanso.tipo == tipo
    ).first()


def iniciar_descanso(usuario_id, tipo, grupo_id=None):
    if tipo not in TIPOS_DESCANSO:
        return False, "Tipo de descanso inválido.", None

    jornada = obtener_jornada_abierta(usuario_id, grupo_id)

    if jornada is None:
        return False, "No tienes una jornada activa.", None

    descanso_activo = obtener_descanso_activo(jornada.id)
    if descanso_activo:
        return False, "Ya tienes un descanso activo.", descanso_activo

    descanso_existente = obtener_descanso_tipo(jornada.id, tipo)
    if descanso_existente:
        return False, "Este descanso ya fue utilizado.", descanso_existente

    descanso = Descanso(
        jornada_id=jornada.id,
        tipo=tipo,
        inicio=obtener_hora_actual()
    )

    db.session.add(descanso)
    db.session.commit()

    return True, "Descanso iniciado correctamente.", descanso


def finalizar_descanso(usuario_id, grupo_id=None):
    jornada = obtener_jornada_abierta(usuario_id, grupo_id)

    if jornada is None:
        return False, "No tienes una jornada activa.", None

    descanso = obtener_descanso_activo(jornada.id)

    if descanso is None:
        return False, "No tienes ningún descanso activo.", None

    duracion_minutos = TIPOS_DESCANSO.get(descanso.tipo)

    if duracion_minutos is None:
        return False, "Tipo de descanso inválido.", None

    hora_actual = obtener_hora_actual()
    fecha_actual = datetime.now(ZONA_HORARIA).date()

    inicio_datetime = datetime.combine(fecha_actual, descanso.inicio)
    actual_datetime = datetime.combine(fecha_actual, hora_actual)

    if actual_datetime < inicio_datetime:
        actual_datetime += timedelta(days=1)

    minutos_transcurridos = (
        actual_datetime - inicio_datetime
    ).total_seconds() / 60

    if minutos_transcurridos < duracion_minutos:
        minutos_faltantes = int(
            duracion_minutos - minutos_transcurridos
        ) + 1

        return (
            False,
            f"El descanso todavía no ha terminado. Faltan aproximadamente {minutos_faltantes} minutos.",
            descanso
        )

    descanso.fin = hora_actual
    db.session.commit()

    return True, "Descanso finalizado correctamente.", descanso
