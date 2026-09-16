from datetime import datetime
from zoneinfo import ZoneInfo

from app import db

from app.models.jornada import Jornada
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


def obtener_hora_extra_activa(usuario_id):

    hora_extra = HoraExtra.query.filter(
        HoraExtra.usuario_id == usuario_id,
        HoraExtra.fin.is_(None)
    ).order_by(
        HoraExtra.inicio.desc()
    ).first()

    return hora_extra


def obtener_ultima_jornada(usuario_id):

    return Jornada.query.filter(
        Jornada.usuario_id == usuario_id,
        Jornada.salida.is_not(None)
    ).order_by(
        Jornada.fecha.desc(),
        Jornada.salida.desc()
    ).first()


def iniciar_hora_extra(
    usuario_id,
    zona_horaria="UTC",
    latitud=None,
    longitud=None,
    direccion=None
):

    # ==========================================
    # VERIFICAR QUE NO TENGA HORAS EXTRAS ACTIVAS
    # ==========================================

    hora_extra_activa = obtener_hora_extra_activa(
        usuario_id
    )

    if hora_extra_activa:

        return (
            False,
            "Ya tienes unas horas extras en curso.",
            hora_extra_activa
        )


    # ==========================================
    # VERIFICAR JORNADA ABIERTA
    # ==========================================

    jornada_abierta = Jornada.query.filter(
        Jornada.usuario_id == usuario_id,
        Jornada.salida.is_(None)
    ).first()

    if jornada_abierta:

        return (
            False,
            "Debes finalizar tu jornada antes de iniciar horas extras.",
            None
        )


    # ==========================================
    # BUSCAR LA ÚLTIMA JORNADA FINALIZADA
    # ==========================================

    jornada = obtener_ultima_jornada(
        usuario_id
    )

    if jornada is None:

        return (
            False,
            "No existe una jornada finalizada para registrar horas extras.",
            None
        )


    # ==========================================
    # HORA Y FECHA ACTUAL
    # ==========================================

    fecha_actual = obtener_fecha_actual(
        zona_horaria
    )

    hora_actual = obtener_hora_actual(
        zona_horaria
    )


    # ==========================================
    # CREAR HORAS EXTRAS
    # ==========================================

    hora_extra = HoraExtra(
        usuario_id=usuario_id,
        jornada_id=jornada.id,
        fecha=fecha_actual,
        inicio=hora_actual,
        fin=None,
        latitud=latitud,
        longitud=longitud,
        direccion=direccion
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
    zona_horaria="UTC"
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


    hora_extra.fin = obtener_hora_actual(
        zona_horaria
    )

    db.session.commit()


    return (
        True,
        "Horas extras finalizadas correctamente.",
        hora_extra
    )
