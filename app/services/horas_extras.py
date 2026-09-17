from datetime import datetime
from zoneinfo import ZoneInfo

from app.extensions import db
from app.models.hora_extra import HoraExtra
from app.models.jornada import Jornada


def obtener_hora_actual(zona_horaria="UTC"):
    """
    Obtiene la hora actual según la zona horaria indicada.
    """
    try:
        zona = ZoneInfo(zona_horaria)
    except Exception:
        zona = ZoneInfo("UTC")

    return datetime.now(zona).time()


def obtener_fecha_actual(zona_horaria="UTC"):
    """
    Obtiene la fecha actual según la zona horaria indicada.
    """
    try:
        zona = ZoneInfo(zona_horaria)
    except Exception:
        zona = ZoneInfo("UTC")

    return datetime.now(zona).date()


def obtener_hora_extra_abierta(usuario_id):
    """
    Busca la última hora extra activa del usuario.
    Una hora extra está activa cuando fin es NULL.
    """
    return HoraExtra.query.filter(
        HoraExtra.usuario_id == usuario_id,
        HoraExtra.fin.is_(None)
    ).order_by(
        HoraExtra.inicio.desc()
    ).first()


def obtener_jornada_del_dia(usuario_id, fecha):
    """
    Busca la jornada correspondiente al usuario y a la fecha indicada.
    """
    return Jornada.query.filter(
        Jornada.usuario_id == usuario_id,
        Jornada.fecha == fecha
    ).order_by(
        Jornada.entrada.desc()
    ).first()


def iniciar_hora_extra(
    usuario_id,
    zona_horaria="UTC",
    latitud=None,
    longitud=None,
    direccion=None
):
    """
    Inicia una hora extra únicamente si el usuario
    tiene una jornada registrada para el día actual.
    """

    # ---------------------------------------------------------
    # 1. Verificar si ya tiene una hora extra abierta
    # ---------------------------------------------------------

    hora_extra_abierta = obtener_hora_extra_abierta(
        usuario_id
    )

    if hora_extra_abierta:

        return (
            None,
            "Ya tienes una hora extra activa."
        )


    # ---------------------------------------------------------
    # 2. Obtener fecha y hora actuales
    # ---------------------------------------------------------

    fecha = obtener_fecha_actual(
        zona_horaria
    )

    hora = obtener_hora_actual(
        zona_horaria
    )


    # ---------------------------------------------------------
    # 3. Buscar la jornada de HOY
    # ---------------------------------------------------------

    jornada = obtener_jornada_del_dia(
        usuario_id,
        fecha
    )


    # ---------------------------------------------------------
    # 4. OBLIGATORIO: debe existir jornada
    # ---------------------------------------------------------

    if jornada is None:

        return (
            None,
            "No puedes iniciar horas extras porque no tienes una jornada registrada para hoy."
        )


    # ---------------------------------------------------------
    # 5. Crear hora extra
    # ---------------------------------------------------------

    hora_extra = HoraExtra(
        usuario_id=usuario_id,

        jornada_id=jornada.id,

        fecha=fecha,

        inicio=hora,

        latitud=latitud,

        longitud=longitud,

        direccion=direccion
    )


    # ---------------------------------------------------------
    # 6. Guardar
    # ---------------------------------------------------------

    db.session.add(
        hora_extra
    )

    db.session.commit()


    return (
        hora_extra,
        "Hora extra iniciada correctamente."
    )



def finalizar_hora_extra(
    usuario_id,
    zona_horaria="UTC"
):
    """
    Finaliza la hora extra activa del usuario.
    """

    hora_extra = obtener_hora_extra_abierta(
        usuario_id
    )

    if hora_extra is None:
        return (
            None,
            "No tienes una hora extra activa."
        )

    # ---------------------------------------------------------
    # Obtener hora actual
    # ---------------------------------------------------------

    hora_extra.fin = obtener_hora_actual(
        zona_horaria
    )

    # ---------------------------------------------------------
    # Guardar cambios
    # ---------------------------------------------------------

    db.session.commit()

    return (
        hora_extra,
        "Hora extra finalizada correctamente."
    )
