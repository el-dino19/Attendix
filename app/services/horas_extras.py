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

    return HoraExtra.query.filter(
        HoraExtra.usuario_id == usuario_id,
        HoraExtra.fin.is_(None)
    ).order_by(
        HoraExtra.inicio.desc()
    ).first()


def obtener_hora_extra_del_dia(
    usuario_id,
    fecha
):

    return HoraExtra.query.filter(
        HoraExtra.usuario_id == usuario_id,
        HoraExtra.fecha == fecha
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
    """
    Inicia una hora extra.

    Reglas:
    - El usuario debe tener una jornada hoy.
    - Solo puede existir una hora extra por día.
    - La hora extra guarda la jornada_id.
    - Guarda latitud, longitud y dirección.
    """

    # ---------------------------------------------------------
    # 1. Obtener fecha y hora actuales
    # ---------------------------------------------------------

    fecha = obtener_fecha_actual(
        zona_horaria
    )

    hora = obtener_hora_actual(
        zona_horaria
    )


    # ---------------------------------------------------------
    # 2. Verificar si ya tiene una hora extra ABIERTA
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
    # 3. Verificar si YA REGISTRÓ una hora extra HOY
    # ---------------------------------------------------------

    hora_extra_del_dia = obtener_hora_extra_del_dia(
        usuario_id,
        fecha
    )

    if hora_extra_del_dia:

        return (
            None,
            "Ya registraste una hora extra el día de hoy."
        )


    # ---------------------------------------------------------
    # 4. Buscar la JORNADA de HOY
    # ---------------------------------------------------------

    jornada = Jornada.query.filter(
        Jornada.usuario_id == usuario_id,
        Jornada.fecha == fecha
    ).first()


    # ---------------------------------------------------------
    # 5. La jornada es obligatoria
    # ---------------------------------------------------------

    if jornada is None:

        return (
            None,
            "No puedes iniciar horas extras porque no tienes una jornada registrada para hoy."
        )


    # ---------------------------------------------------------
    # 6. Crear hora extra
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
    # 7. Guardar
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
