from datetime import datetime
from zoneinfo import ZoneInfo

from app.extensions import db
from app.models.hora_extra import HoraExtra


# =========================================================
# HORA ACTUAL
# =========================================================

def obtener_hora_actual(zona_horaria="UTC"):

    try:
        zona = ZoneInfo(zona_horaria)
    except Exception:
        zona = ZoneInfo("UTC")

    return datetime.now(zona).time()


# =========================================================
# OBTENER HORA EXTRA ABIERTA
# =========================================================

def obtener_hora_extra_abierta(usuario_id):

    hora_extra = HoraExtra.query.filter(
        HoraExtra.usuario_id == usuario_id,
        HoraExtra.salida.is_(None)
    ).order_by(
        HoraExtra.entrada.desc()
    ).first()

    return hora_extra


# =========================================================
# INICIAR HORA EXTRA
# =========================================================

def iniciar_hora_extra(
    usuario_id,
    zona_horaria="UTC",
    latitud=None,
    longitud=None,
    direccion=None
):

    # Verificar que no tenga una hora extra abierta

    hora_extra_abierta = obtener_hora_extra_abierta(
        usuario_id
    )

    if hora_extra_abierta:
        return None, "Ya tienes una hora extra activa."


    try:
        zona = ZoneInfo(zona_horaria)
    except Exception:
        zona = ZoneInfo("UTC")


    ahora = datetime.now(zona)


    hora_extra = HoraExtra(
        usuario_id=usuario_id,
        fecha=ahora.date(),
        entrada=ahora.time(),
        latitud=latitud,
        longitud=longitud,
        direccion=direccion
    )


    db.session.add(hora_extra)
    db.session.commit()


    return hora_extra, "Hora extra iniciada correctamente."


# =========================================================
# FINALIZAR HORA EXTRA
# =========================================================

def finalizar_hora_extra(
    usuario_id,
    zona_horaria="UTC"
):

    hora_extra = obtener_hora_extra_abierta(
        usuario_id
    )


    if hora_extra is None:

        return None, "No tienes una hora extra activa."


    hora_extra.salida = obtener_hora_actual(
        zona_horaria
    )


    db.session.commit()


    return hora_extra, "Hora extra finalizada correctamente."