from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import (
    Font,
    PatternFill,
    Alignment,
    Border,
    Side
)
from openpyxl.utils import get_column_letter


def generar_excel_asistencia(registros):

    libro = Workbook()

    hoja = libro.active

    hoja.title = "Asistencia"


    # ==========================================
    # ENCABEZADOS
    # ==========================================

    encabezados = [
        "ID Jornada",
        "Empleado",
        "Correo",
        "Fecha",
        "Entrada",
        "Break mañana",
        "Lunch",
        "Break tarde",
        "Salida"
    ]

    hoja.append(encabezados)


    # ==========================================
    # ESTILO ENCABEZADOS
    # ==========================================

    color_azul = "0D6EFD"

    fondo = PatternFill(
        fill_type="solid",
        fgColor=color_azul
    )

    borde = Border(
        bottom=Side(
            style="thin",
            color="FFFFFF"
        )
    )

    for celda in hoja[1]:

        celda.font = Font(
            bold=True,
            color="FFFFFF"
        )

        celda.fill = fondo

        celda.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

        celda.border = borde


    # ==========================================
    # FORMATO HORA
    # ==========================================

    def formato_hora(hora):

        if hora is None:
            return ""

        return hora.strftime("%H:%M:%S")


    # ==========================================
    # FORMATO DESCANSO
    # ==========================================

    def formato_descanso(descanso):

        if descanso is None:
            return ""

        inicio = formato_hora(
            descanso.inicio
        )

        if descanso.fin:

            fin = formato_hora(
                descanso.fin
            )

        else:

            fin = "En curso"

        return f"{inicio} - {fin}"


    # ==========================================
    # RECORRER JORNADAS
    # ==========================================

    for jornada in registros:

        usuario = jornada.usuario

        if usuario is None:
            continue


        # ======================================
        # NO EXPORTAR ADMIN
        # ======================================

        if str(usuario.rol).strip().lower() == "admin":
            continue


        break_manana = None
        lunch = None
        break_tarde = None


        # ======================================
        # BUSCAR DESCANSOS
        # ======================================

        for descanso in jornada.descansos:

            if descanso.tipo == "break_manana":

                break_manana = descanso

            elif descanso.tipo == "lunch":

                lunch = descanso

            elif descanso.tipo == "break_tarde":

                break_tarde = descanso


        # ======================================
        # AGREGAR FILA
        # ======================================

        hoja.append([

            jornada.id,

            usuario.nombre,

            usuario.correo,

            jornada.fecha.strftime(
                "%Y-%m-%d"
            )
            if jornada.fecha
            else "",

            formato_hora(
                jornada.entrada
            ),

            formato_descanso(
                break_manana
            ),

            formato_descanso(
                lunch
            ),

            formato_descanso(
                break_tarde
            ),

            formato_hora(
                jornada.salida
            )

        ])


    # ==========================================
    # AJUSTAR COLUMNAS
    # ==========================================

    anchos = {
        1: 14,
        2: 25,
        3: 35,
        4: 15,
        5: 15,
        6: 22,
        7: 22,
        8: 22,
        9: 15
    }

    for numero_columna, ancho in anchos.items():

        letra = get_column_letter(
            numero_columna
        )

        hoja.column_dimensions[
            letra
        ].width = ancho


    # ==========================================
    # CENTRAR COLUMNAS
    # ==========================================

    for fila in hoja.iter_rows(
        min_row=2
    ):

        for indice in [
            0, 3, 4, 5, 6, 7, 8
        ]:

            fila[indice].alignment = Alignment(
                horizontal="center"
            )


    # ==========================================
    # CONGELAR ENCABEZADO
    # ==========================================

    hoja.freeze_panes = "A2"


    # ==========================================
    # FILTRO
    # ==========================================

    hoja.auto_filter.ref = hoja.dimensions


    # ==========================================
    # ALTURA ENCABEZADO
    # ==========================================

    hoja.row_dimensions[1].height = 25


    # ==========================================
    # CREAR ARCHIVO
    # ==========================================

    archivo = BytesIO()

    libro.save(archivo)

    archivo.seek(0)

    return archivo
