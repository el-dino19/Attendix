from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app import db
from app.models.descanso import Descanso
from app.models.jornada import Jornada


ZONA_HORARIA = ZoneInfo("America/Chicago")


# ==========================================
# DURACIÓN DE CADA DESCANSO
# ==========================================

TIPOS_DESCANSO = {
    "break_manana": 15,
    "lunch": 60,
    "break_tarde": 15
}


# ==========================================
# HORA ACTUAL
# ==========================================

def obtener_hora_actual():

    ahora = datetime.now(
        ZONA_HORARIA
    )

    return ahora.time()


# ==========================================
# BUSCAR JORNADA ACTIVA
# ==========================================

def obtener_jornada_abierta(usuario_id):

    jornada = Jornada.query.filter(
        Jornada.usuario_id == usuario_id,
        Jornada.salida.is_(None)
    ).order_by(
        Jornada.entrada.desc()
    ).first()

    return jornada


# ==========================================
# BUSCAR DESCANSO ACTIVO
# ==========================================

def obtener_descanso_activo(jornada_id):

    descanso = Descanso.query.filter(
        Descanso.jornada_id == jornada_id,
        Descanso.fin.is_(None)
    ).first()

    return descanso


# ==========================================
# BUSCAR DESCANSO DEL MISMO TIPO
# ==========================================

def obtener_descanso_tipo(
    jornada_id,
    tipo
):

    descanso = Descanso.query.filter(
        Descanso.jornada_id == jornada_id,
        Descanso.tipo == tipo
    ).first()

    return descanso


# ==========================================
# INICIAR DESCANSO
# ==========================================

def iniciar_descanso(
    usuario_id,
    tipo
):

    # --------------------------------------
    # VALIDAR TIPO
    # --------------------------------------

    if tipo not in TIPOS_DESCANSO:

        return (
            False,
            "Tipo de descanso inválido.",
            None
        )


    # --------------------------------------
    # BUSCAR JORNADA
    # --------------------------------------

    jornada = obtener_jornada_abierta(
        usuario_id
    )


    if jornada is None:

        return (
            False,
            "No tienes una jornada activa.",
            None
        )


    # --------------------------------------
    # VERIFICAR DESCANSO ACTIVO
    # --------------------------------------

    descanso_activo = obtener_descanso_activo(
        jornada.id
    )


    if descanso_activo:

        return (
            False,
            "Ya tienes un descanso activo.",
            descanso_activo
        )


    # --------------------------------------
    # VERIFICAR SI YA UTILIZÓ ESE DESCANSO
    # --------------------------------------

    descanso_existente = obtener_descanso_tipo(
        jornada.id,
        tipo
    )


    if descanso_existente:

        return (
            False,
            "Este descanso ya fue utilizado.",
            descanso_existente
        )


    # --------------------------------------
    # CREAR DESCANSO
    # --------------------------------------

    descanso = Descanso(
        jornada_id=jornada.id,
        tipo=tipo,
        inicio=obtener_hora_actual()
    )


    db.session.add(descanso)

    db.session.commit()


    return (
        True,
        "Descanso iniciado correctamente.",
        descanso
    )


# ==========================================
# FINALIZAR DESCANSO
# ==========================================

def finalizar_descanso(usuario_id):

    # --------------------------------------
    # BUSCAR JORNADA
    # --------------------------------------

    jornada = obtener_jornada_abierta(
        usuario_id
    )


    if jornada is None:

        return (
            False,
            "No tienes una jornada activa.",
            None
        )


    # --------------------------------------
    # BUSCAR DESCANSO ACTIVO
    # --------------------------------------

    descanso = obtener_descanso_activo(
        jornada.id
    )


    if descanso is None:

        return (
            False,
            "No tienes ningún descanso activo.",
            None
        )


    # --------------------------------------
    # DURACIÓN PERMITIDA
    # --------------------------------------

    duracion_minutos = TIPOS_DESCANSO.get(
        descanso.tipo
    )


    if duracion_minutos is None:

        return (
            False,
            "Tipo de descanso inválido.",
            None
        )


    # --------------------------------------
    # HORA ACTUAL
    # --------------------------------------

    hora_actual = obtener_hora_actual()


    # --------------------------------------
    # CONVERTIR HORAS A DATETIME
    # --------------------------------------

    fecha_actual = datetime.now(
        ZONA_HORARIA
    ).date()


    inicio_datetime = datetime.combine(
        fecha_actual,
        descanso.inicio
    )


    actual_datetime = datetime.combine(
        fecha_actual,
        hora_actual
    )


    # --------------------------------------
    # MANEJAR CAMBIO DE MEDIANOCHE
    # --------------------------------------

    if actual_datetime < inicio_datetime:

        actual_datetime += timedelta(
            days=1
        )


    # --------------------------------------
    # CALCULAR TIEMPO TRANSCURRIDO
    # --------------------------------------

    tiempo_transcurrido = (
        actual_datetime -
        inicio_datetime
    )


    minutos_transcurridos = (
        tiempo_transcurrido.total_seconds()
        / 60
    )


    # --------------------------------------
    # VERIFICAR DURACIÓN
    # --------------------------------------

    if minutos_transcurridos < duracion_minutos:

        minutos_faltantes = (
            duracion_minutos -
            minutos_transcurridos
        )


        minutos_faltantes = int(
            minutos_faltantes
        ) + 1


        return (
            False,
            (
                f"El descanso todavía no ha terminado. "
                f"Faltan aproximadamente "
                f"{minutos_faltantes} minutos."
            ),
            descanso
        )


    # --------------------------------------
    # REGISTRAR FIN
    # --------------------------------------

    descanso.fin = hora_actual


    db.session.commit()


    return (
        True,
        "Descanso finalizado correctamente.",
        descanso
    )