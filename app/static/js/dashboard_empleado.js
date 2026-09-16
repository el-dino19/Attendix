// ==========================================
// DASHBOARD EMPLEADO
// CONTADOR DE DESCANSOS
// ==========================================

document.addEventListener("DOMContentLoaded", function () {

    const contador = document.getElementById("contador");

    // No existe descanso activo
    if (!contador) {
        return;
    }


    // ==========================================
    // ELEMENTOS
    // ==========================================

    const mensaje =
        document.getElementById("mensaje-contador");

    const formulario =
        document.getElementById("form-finalizar-descanso");

    const boton =
        document.getElementById("btn-finalizar-descanso");


    // ==========================================
    // DATOS DEL DESCANSO
    // ==========================================

    const tipoDescanso =
        (contador.dataset.tipo || "").trim();

    const horaInicio =
        (contador.dataset.inicio || "").trim();


    console.log("Tipo de descanso:", tipoDescanso);
    console.log("Hora de inicio:", horaInicio);


    // ==========================================
    // DURACIONES
    // ==========================================

    const duraciones = {

        break_manana: 15 * 60,

        lunch: 60 * 60,

        break_tarde: 15 * 60

    };


    const duracionTotal =
        duraciones[tipoDescanso];


    // ==========================================
    // VALIDAR TIPO
    // ==========================================

    if (!duracionTotal) {

        console.error(
            "Tipo de descanso no válido:",
            tipoDescanso
        );

        contador.textContent = "00:00";

        if (mensaje) {
            mensaje.textContent =
                "Tipo de descanso no válido.";
        }

        return;
    }


    // ==========================================
    // CONVERTIR HORA A SEGUNDOS
    // ==========================================

    function convertirHoraASegundos(hora) {

        const partes = hora.split(":");


        if (partes.length !== 3) {

            console.error(
                "Formato de hora incorrecto:",
                hora
            );

            return null;
        }


        const horas =
            Number(partes[0]);

        const minutos =
            Number(partes[1]);

        const segundos =
            Number(partes[2]);


        if (
            Number.isNaN(horas) ||
            Number.isNaN(minutos) ||
            Number.isNaN(segundos)
        ) {

            return null;
        }


        return (
            horas * 3600 +
            minutos * 60 +
            segundos
        );
    }


    // ==========================================
    // HORA DE INICIO
    // ==========================================

    const inicioSegundos =
        convertirHoraASegundos(
            horaInicio
        );


    if (inicioSegundos === null) {

        contador.textContent = "00:00";

        if (mensaje) {
            mensaje.textContent =
                "No se pudo calcular el tiempo.";
        }

        return;
    }


    // ==========================================
    // OBTENER HORA ACTUAL
    // ==========================================

    function obtenerHoraActualSegundos() {

        const ahora = new Date();

        return (
            ahora.getHours() * 3600 +
            ahora.getMinutes() * 60 +
            ahora.getSeconds()
        );
    }


    // ==========================================
    // TIEMPO TRANSCURRIDO
    // ==========================================

    function obtenerTiempoTranscurrido() {

        const actual =
            obtenerHoraActualSegundos();


        let diferencia =
            actual - inicioSegundos;


        /*
         * Si cruza medianoche,
         * ajustamos las 24 horas.
         */

        if (diferencia < 0) {

            diferencia +=
                24 * 60 * 60;
        }


        return diferencia;
    }


    // ==========================================
    // FORMATEAR
    // ==========================================

    function formatearTiempo(segundos) {

        segundos =
            Math.max(
                0,
                Math.floor(segundos)
            );


        const minutos =
            Math.floor(
                segundos / 60
            );


        const segundosRestantes =
            segundos % 60;


        return (
            String(minutos).padStart(2, "0")
            +
            ":"
            +
            String(segundosRestantes).padStart(2, "0")
        );
    }


    // ==========================================
    // ACTUALIZAR CONTADOR
    // ==========================================

    function actualizarContador() {

        const transcurrido =
            obtenerTiempoTranscurrido();


        const restante =
            duracionTotal -
            transcurrido;


        // ======================================
        // TIEMPO TERMINADO
        // ======================================

        if (restante <= 0) {

            contador.textContent =
                "00:00";


            if (mensaje) {

                mensaje.textContent =
                    "El tiempo del descanso ha terminado. Pulsa finalizar para registrar la hora.";
            }


            /*
             * IMPORTANTE:
             *
             * NO enviamos el formulario.
             *
             * El descanso solamente termina
             * cuando el empleado pulsa el botón.
             */

            return;
        }


        // ======================================
        // MOSTRAR TIEMPO
        // ======================================

        contador.textContent =
            formatearTiempo(
                restante
            );


        if (mensaje) {

            mensaje.textContent =
                "Descanso en progreso";
        }
    }


    // ==========================================
    // PRIMERA EJECUCIÓN
    // ==========================================

    actualizarContador();


    // ==========================================
    // ACTUALIZAR CADA SEGUNDO
    // ==========================================

    const intervalo =
        setInterval(
            actualizarContador,
            1000
        );


    // ==========================================
    // FINALIZAR MANUALMENTE
    // ==========================================

    if (formulario && boton) {

        formulario.addEventListener(
            "submit",
            function () {

                /*
                 * El botón es quien realmente
                 * registra el fin del descanso.
                 */

                boton.disabled = true;

                boton.textContent =
                    "FINALIZANDO...";


                clearInterval(intervalo);
            }
        );
    }

});