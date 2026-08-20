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

    # ==========================================
    # CREAR LIBRO
    # ==========================================

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
    # FUNCION PARA FORMATEAR HORAS
    # ==========================================

    def formato_hora(hora):

        if hora is None:
            return ""

        return hora.strftime("%H:%M:%S")


    # ==========================================
    # FUNCION PARA FORMATEAR DESCANSO
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


        break_manana = None

        lunch = None

        break_tarde = None


        # ======================================
        # BUSCAR LOS DESCANSOS
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

            usuario.nombre
            if usuario
            else "",

            usuario.correo
            if usuario
            else "",

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
    # CENTRAR ALGUNAS COLUMNAS
    # ==========================================

    for fila in hoja.iter_rows(
        min_row=2
    ):

        fila[0].alignment = Alignment(
            horizontal="center"
        )

        fila[3].alignment = Alignment(
            horizontal="center"
        )

        fila[4].alignment = Alignment(
            horizontal="center"
        )

        fila[5].alignment = Alignment(
            horizontal="center"
        )

        fila[6].alignment = Alignment(
            horizontal="center"
        )

        fila[7].alignment = Alignment(
            horizontal="center"
        )

        fila[8].alignment = Alignment(
            horizontal="center"
        )


    # ==========================================
    # CONGELAR ENCABEZADO
    # ==========================================

    hoja.freeze_panes = "A2"


    # ==========================================
    # FILTRO AUTOMÁTICO
    # ==========================================

    hoja.auto_filter.ref = hoja.dimensions


    # ==========================================
    # ALTURA DEL ENCABEZADO
    # ==========================================

    hoja.row_dimensions[1].height = 25


    # ==========================================
    # CREAR ARCHIVO EN MEMORIA
    # ==========================================

    archivo = BytesIO()

    libro.save(archivo)

    archivo.seek(0)


    return archivo