// ============================================================
// DASHBOARD EMPLEADO
// - Contador de descansos
// - Contador de horas extras
// - Solicitud de ubicación GPS
// - Inicio de horas extras con GPS
// - Finalización de horas extras con GPS
// ============================================================


// ============================================================
// VARIABLES GLOBALES
// ============================================================

let ubicacionActual = null;


// ============================================================
// OBTENER UBICACIÓN DEL USUARIO
// ============================================================

function obtenerUbicacion() {

    return new Promise(function (resolve, reject) {

        if (!navigator.geolocation) {

            reject(
                new Error(
                    "Tu navegador no soporta la ubicación GPS."
                )
            );

            return;
        }


        navigator.geolocation.getCurrentPosition(

            function (position) {

                const ubicacion = {

                    latitud:
                        position.coords.latitude,

                    longitud:
                        position.coords.longitude
                };


                // Guardamos la última ubicación conocida

                ubicacionActual = ubicacion;


                console.log(
                    "Ubicación obtenida:",
                    ubicacion
                );


                resolve(ubicacion);
            },


            function (error) {

                console.error(
                    "Error obteniendo ubicación:",
                    error
                );


                let mensaje =
                    "No fue posible obtener tu ubicación.";


                switch (error.code) {

                    case error.PERMISSION_DENIED:

                        mensaje =
                            "Debes permitir el acceso a tu ubicación para registrar las horas extras.";

                        break;


                    case error.POSITION_UNAVAILABLE:

                        mensaje =
                            "No se pudo determinar tu ubicación.";

                        break;


                    case error.TIMEOUT:

                        mensaje =
                            "La ubicación tardó demasiado en responder.";

                        break;
                }


                reject(
                    new Error(mensaje)
                );
            },


            {
                enableHighAccuracy: true,

                timeout: 15000,

                maximumAge: 0
            }
        );

    });
}


// ============================================================
// SOLICITAR UBICACIÓN AL ENTRAR AL DASHBOARD
// ============================================================

function solicitarUbicacionInicial() {

    if (!navigator.geolocation) {

        console.warn(
            "El navegador no soporta geolocalización."
        );

        return;
    }


    navigator.geolocation.getCurrentPosition(

        function (position) {

            ubicacionActual = {

                latitud:
                    position.coords.latitude,

                longitud:
                    position.coords.longitude
            };


            console.log(
                "Permiso de ubicación concedido."
            );


            console.log(
                "Ubicación:",
                ubicacionActual
            );
        },


        function (error) {

            console.warn(
                "El usuario no permitió la ubicación:",
                error
            );
        },


        {
            enableHighAccuracy: true,

            timeout: 15000,

            maximumAge: 0
        }
    );
}


// ============================================================
// CONTADOR DE DESCANSOS
// ============================================================

function iniciarContadorDescanso() {

    const contador =
        document.getElementById(
            "contador"
        );


    // No existe descanso activo

    if (!contador) {
        return;
    }


    // ========================================================
    // ELEMENTOS
    // ========================================================

    const mensaje =
        document.getElementById(
            "mensaje-contador"
        );


    const formulario =
        document.getElementById(
            "form-finalizar-descanso"
        );


    const boton =
        document.getElementById(
            "btn-finalizar-descanso"
        );


    // ========================================================
    // DATOS
    // ========================================================

    const tipoDescanso =
        (
            contador.dataset.tipo ||
            ""
        ).trim();


    const horaInicio =
        (
            contador.dataset.inicio ||
            ""
        ).trim();


    console.log(
        "Tipo de descanso:",
        tipoDescanso
    );


    console.log(
        "Hora de inicio:",
        horaInicio
    );


    // ========================================================
    // DURACIONES
    // ========================================================

    const duraciones = {

        break_manana:
            15 * 60,

        lunch:
            60 * 60,

        break_tarde:
            15 * 60
    };


    const duracionTotal =
        duraciones[
            tipoDescanso
        ];


    // ========================================================
    // VALIDAR TIPO
    // ========================================================

    if (!duracionTotal) {

        console.error(
            "Tipo de descanso no válido:",
            tipoDescanso
        );


        contador.textContent =
            "00:00";


        if (mensaje) {

            mensaje.textContent =
                "Tipo de descanso no válido.";
        }


        return;
    }


    // ========================================================
    // CONVERTIR HORA A SEGUNDOS
    // ========================================================

    function convertirHoraASegundos(hora) {

        const partes =
            hora.split(":");


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


    // ========================================================
    // HORA INICIO
    // ========================================================

    const inicioSegundos =
        convertirHoraASegundos(
            horaInicio
        );


    if (inicioSegundos === null) {

        contador.textContent =
            "00:00";


        if (mensaje) {

            mensaje.textContent =
                "No se pudo calcular el tiempo.";
        }


        return;
    }


    // ========================================================
    // HORA ACTUAL
    // ========================================================

    function obtenerHoraActualSegundos() {

        const ahora =
            new Date();


        return (
            ahora.getHours() * 3600 +
            ahora.getMinutes() * 60 +
            ahora.getSeconds()
        );
    }


    // ========================================================
    // TIEMPO TRANSCURRIDO
    // ========================================================

    function obtenerTiempoTranscurrido() {

        const actual =
            obtenerHoraActualSegundos();


        let diferencia =
            actual -
            inicioSegundos;


        /*
         * Si el descanso cruza medianoche,
         * corregimos la diferencia.
         */

        if (diferencia < 0) {

            diferencia +=
                24 * 60 * 60;
        }


        return diferencia;
    }


    // ========================================================
    // FORMATEAR TIEMPO
    // ========================================================

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

            String(minutos)
                .padStart(2, "0")

            +

            ":"

            +

            String(segundosRestantes)
                .padStart(2, "0")
        );
    }


    // ========================================================
    // ACTUALIZAR CONTADOR
    // ========================================================

    function actualizarContador() {

        const transcurrido =
            obtenerTiempoTranscurrido();


        const restante =
            duracionTotal -
            transcurrido;


        // ====================================================
        // TIEMPO TERMINADO
        // ====================================================

        if (restante <= 0) {

            contador.textContent =
                "00:00";


            if (mensaje) {

                mensaje.textContent =
                    "El tiempo del descanso ha terminado. Pulsa finalizar para registrar la hora.";
            }


            return;
        }


        // ====================================================
        // MOSTRAR TIEMPO
        // ====================================================

        contador.textContent =
            formatearTiempo(
                restante
            );


        if (mensaje) {

            mensaje.textContent =
                "Descanso en progreso";
        }
    }


    // ========================================================
    // PRIMERA EJECUCIÓN
    // ========================================================

    actualizarContador();


    // ========================================================
    // ACTUALIZAR CADA SEGUNDO
    // ========================================================

    const intervalo =
        setInterval(
            actualizarContador,
            1000
        );


    // ========================================================
    // FINALIZACIÓN MANUAL
    // ========================================================

    if (formulario) {

        formulario.addEventListener(
            "submit",
            function () {

                if (boton) {

                    boton.disabled =
                        true;


                    boton.textContent =
                        "FINALIZANDO...";
                }


                clearInterval(
                    intervalo
                );
            }
        );
    }
}


// ============================================================
// CONTADOR DE HORAS EXTRAS
// ============================================================

function iniciarContadorHorasExtras() {

    const contador =
        document.getElementById(
            "contador-horas-extras"
        );


    // No hay horas extras activas

    if (!contador) {
        return;
    }


    const inicioTexto =
        contador.dataset.inicio;


    if (!inicioTexto) {

        console.error(
            "No existe la fecha de inicio de las horas extras."
        );

        return;
    }


    // ========================================================
    // CONVERTIR FECHA
    // ========================================================

    const inicio =
        new Date(
            inicioTexto
        );


    if (Number.isNaN(inicio.getTime())) {

        console.error(
            "Fecha de inicio inválida:",
            inicioTexto
        );

        contador.textContent =
            "00:00:00";

        return;
    }


    // ========================================================
    // ACTUALIZAR
    // ========================================================

    function actualizarContador() {

        const ahora =
            new Date();


        let segundos =
            Math.floor(
                (
                    ahora.getTime() -
                    inicio.getTime()
                ) / 1000
            );


        if (segundos < 0) {

            segundos = 0;
        }


        const horas =
            Math.floor(
                segundos / 3600
            );


        const minutos =
            Math.floor(
                (segundos % 3600) / 60
            );


        const segundosRestantes =
            segundos % 60;


        contador.textContent =

            String(horas)
                .padStart(2, "0")

            +

            ":"

            +

            String(minutos)
                .padStart(2, "0")

            +

            ":"

            +

            String(segundosRestantes)
                .padStart(2, "0");
    }


    // Primera ejecución

    actualizarContador();


    // Cada segundo

    setInterval(
        actualizarContador,
        1000
    );
}


// ============================================================
// INICIAR HORAS EXTRAS
// ============================================================

async function iniciarHorasExtras() {

    try {

        // ====================================================
        // OBTENER GPS ACTUAL
        // ====================================================

        const ubicacion =
            await obtenerUbicacion();


        // ====================================================
        // DESHABILITAR BOTÓN
        // ====================================================

        const boton =
            document.querySelector(
                '[onclick="iniciarHorasExtras()"]'
            );


        if (boton) {

            boton.disabled =
                true;

            boton.style.opacity =
                "0.6";

            boton.style.pointerEvents =
                "none";
        }


        // ====================================================
        // ENVIAR AL SERVIDOR
        // ====================================================

        const response =
            await fetch(
                "/Attendix/horas-extras/iniciar",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    credentials:
                        "same-origin",

                    body:
                        JSON.stringify({

                            latitud:
                                ubicacion.latitud,

                            longitud:
                                ubicacion.longitud
                        })
                }
            );


        // ====================================================
        // RESPUESTA
        // ====================================================

        const resultado =
            await response.json();


        if (
            !response.ok ||
            !resultado.ok
        ) {

            throw new Error(
                resultado.mensaje ||
                "No se pudieron iniciar las horas extras."
            );
        }


        // ====================================================
        // ÉXITO
        // ====================================================

        console.log(
            "Horas extras iniciadas:",
            resultado
        );


        window.location.reload();
    }


    catch (error) {

        console.error(
            "Error iniciando horas extras:",
            error
        );


        alert(
            error.message ||
            "No fue posible iniciar las horas extras."
        );


        // ====================================================
        // RESTAURAR BOTÓN
        // ====================================================

        const boton =
            document.querySelector(
                '[onclick="iniciarHorasExtras()"]'
            );


        if (boton) {

            boton.disabled =
                false;

            boton.style.opacity =
                "";

            boton.style.pointerEvents =
                "";
        }
    }
}


// ============================================================
// FINALIZAR HORAS EXTRAS
// ============================================================

async function finalizarHorasExtras() {

    const confirmar =
        confirm(
            "¿Estás seguro de que deseas finalizar las horas extras?"
        );


    if (!confirmar) {
        return;
    }


    try {

        // ====================================================
        // OBTENER GPS ACTUAL
        // ====================================================

        const ubicacion =
            await obtenerUbicacion();


        // ====================================================
        // BOTÓN
        // ====================================================

        const boton =
            document.querySelector(
                '[onclick="finalizarHorasExtras()"]'
            );


        if (boton) {

            boton.disabled =
                true;

            boton.textContent =
                "FINALIZANDO...";

            boton.style.opacity =
                "0.6";
        }


        // ====================================================
        // ENVIAR AL SERVIDOR
        // ====================================================

        const response =
            await fetch(
                "/Attendix/horas-extras/finalizar",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    credentials:
                        "same-origin",

                    body:
                        JSON.stringify({

                            latitud:
                                ubicacion.latitud,

                            longitud:
                                ubicacion.longitud
                        })
                }
            );


        // ====================================================
        // RESPUESTA
        // ====================================================

        const resultado =
            await response.json();


        if (
            !response.ok ||
            !resultado.ok
        ) {

            throw new Error(
                resultado.mensaje ||
                "No se pudieron finalizar las horas extras."
            );
        }


        // ====================================================
        // MOSTRAR RESULTADO
        // ====================================================

        const minutos =
            resultado.minutos_totales;


        let mensaje =
            resultado.mensaje ||
            "Horas extras finalizadas correctamente.";


        if (
            minutos !== undefined &&
            minutos !== null
        ) {

            mensaje +=
                "\n\nTiempo trabajado: " +
                minutos +
                " minutos.";
        }


        alert(
            mensaje
        );


        // ====================================================
        // ACTUALIZAR DASHBOARD
        // ====================================================

        window.location.reload();
    }


    catch (error) {

        console.error(
            "Error finalizando horas extras:",
            error
        );


        alert(
            error.message ||
            "No fue posible finalizar las horas extras."
        );


        // ====================================================
        // RESTAURAR BOTÓN
        // ====================================================

        const boton =
            document.querySelector(
                '[onclick="finalizarHorasExtras()"]'
            );


        if (boton) {

            boton.disabled =
                false;

            boton.innerHTML =
                '<i class="bi bi-stop-circle-fill"></i> FINALIZAR HORAS EXTRAS';

            boton.style.opacity =
                "";
        }
    }
}


// ============================================================
// INICIALIZAR TODO EL DASHBOARD
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        console.log(
            "Dashboard de empleado cargado."
        );


        // ====================================================
        // SOLICITAR UBICACIÓN
        // ====================================================

        solicitarUbicacionInicial();


        // ====================================================
        // CONTADOR DESCANSO
        // ====================================================

        iniciarContadorDescanso();


        // ====================================================
        // CONTADOR HORAS EXTRAS
        // ====================================================

        iniciarContadorHorasExtras();
    }
);
