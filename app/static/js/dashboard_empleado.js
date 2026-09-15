// =========================================================
// DASHBOARD EMPLEADO - ATTENDIX
// =========================================================


// =========================================================
// INICIO DEL DASHBOARD
// =========================================================

document.addEventListener("DOMContentLoaded", function () {


    // =====================================================
    // RELOJ DIGITAL
    // =====================================================

    function actualizarReloj() {

        const reloj =
            document.getElementById("reloj");

        const fecha =
            document.getElementById("fecha-actual");


        if (!reloj) {
            return;
        }


        const ahora =
            new Date();


        // -------------------------------------------------
        // HORA COLOMBIA
        // -------------------------------------------------

        const opcionesHora = {

            timeZone: "America/Bogota",

            hour: "2-digit",

            minute: "2-digit",

            second: "2-digit",

            hour12: true

        };


        // -------------------------------------------------
        // FECHA COLOMBIA
        // -------------------------------------------------

        const opcionesFecha = {

            timeZone: "America/Bogota",

            weekday: "long",

            year: "numeric",

            month: "long",

            day: "numeric"

        };


        const horaColombia =
            new Intl.DateTimeFormat(
                "es-CO",
                opcionesHora
            ).format(ahora);


        const fechaColombia =
            new Intl.DateTimeFormat(
                "es-CO",
                opcionesFecha
            ).format(ahora);


        reloj.textContent =
            horaColombia;


        if (fecha) {

            fecha.textContent =
                fechaColombia;

        }

    }


    // Ejecutar inmediatamente

    actualizarReloj();


    // Actualizar cada segundo

    setInterval(
        actualizarReloj,
        1000
    );



    // =====================================================
    // MENSAJES FLASH
    // =====================================================

    const mensajes =
        document.querySelectorAll(
            ".custom-toast"
        );


    mensajes.forEach(function (mensaje) {


        setTimeout(function () {


            mensaje.classList.add(
                "toast-hide"
            );


            setTimeout(function () {

                mensaje.remove();

            }, 400);


        }, 4000);

    });



    // =====================================================
    // CONTADOR DE DESCANSO
    // =====================================================

    const contador =
        document.getElementById(
            "contador"
        );


    if (contador) {

        iniciarContadorDescanso(
            contador
        );

    }



    // =====================================================
    // CONTADOR DE HORAS EXTRAS
    // =====================================================

    const contadorHorasExtras =
        document.getElementById(
            "contador-horas-extras"
        );


    if (contadorHorasExtras) {

        iniciarContadorHorasExtras(
            contadorHorasExtras
        );

    }



    // =====================================================
    // UBICACIÓN DEL USUARIO
    // =====================================================

    obtenerUbicacionUsuario();



});



// =========================================================
// CONTADOR DE DESCANSO
// =========================================================

function iniciarContadorDescanso(
    contador
) {


    const mensaje =
        document.getElementById(
            "mensaje-contador"
        );


    const tipo =
        (
            contador.dataset.tipo ||
            ""
        ).trim();


    const horaInicio =
        (
            contador.dataset.inicio ||
            ""
        ).trim();



    // =====================================================
    // DURACIONES
    // =====================================================

    const duraciones = {

        break_manana:
            15 * 60,

        lunch:
            60 * 60,

        break_tarde:
            15 * 60

    };


    const duracionTotal =
        duraciones[tipo];


    if (!duracionTotal) {


        contador.textContent =
            "00:00";


        if (mensaje) {

            mensaje.textContent =
                "Tipo de descanso no válido.";

        }


        return;

    }



    // =====================================================
    // CONVERTIR HORA A SEGUNDOS
    // =====================================================

    function convertirHoraASegundos(
        hora
    ) {


        const partes =
            hora.split(":");


        if (
            partes.length !== 3
        ) {

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



    const inicioSegundos =
        convertirHoraASegundos(
            horaInicio
        );


    if (
        inicioSegundos === null
    ) {


        contador.textContent =
            "00:00";


        if (mensaje) {

            mensaje.textContent =
                "No se pudo calcular el tiempo.";

        }


        return;

    }



    // =====================================================
    // HORA ACTUAL DE COLOMBIA
    // =====================================================

    function obtenerHoraActualSegundos() {


        const ahora =
            new Date();


        const partes =
            new Intl.DateTimeFormat(
                "en-US",
                {

                    timeZone:
                        "America/Bogota",

                    hour:
                        "2-digit",

                    minute:
                        "2-digit",

                    second:
                        "2-digit",

                    hour12:
                        false

                }
            ).formatToParts(ahora);



        let horas = 0;

        let minutos = 0;

        let segundos = 0;



        partes.forEach(
            function (parte) {


                if (
                    parte.type === "hour"
                ) {

                    horas =
                        Number(
                            parte.value
                        );

                }


                if (
                    parte.type === "minute"
                ) {

                    minutos =
                        Number(
                            parte.value
                        );

                }


                if (
                    parte.type === "second"
                ) {

                    segundos =
                        Number(
                            parte.value
                        );

                }

            }
        );


        return (

            horas * 3600 +

            minutos * 60 +

            segundos

        );

    }



    // =====================================================
    // TIEMPO TRANSCURRIDO
    // =====================================================

    function obtenerTiempoTranscurrido() {


        const actual =
            obtenerHoraActualSegundos();


        let diferencia =
            actual -
            inicioSegundos;


        // Cambio de día

        if (
            diferencia < 0
        ) {

            diferencia +=
                24 * 60 * 60;

        }


        return diferencia;

    }



    // =====================================================
    // FORMATEAR TIEMPO
    // =====================================================

    function formatearTiempo(
        segundos
    ) {


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

            String(
                minutos
            ).padStart(2, "0") +

            ":" +

            String(
                segundosRestantes
            ).padStart(2, "0")

        );

    }



    // =====================================================
    // ACTUALIZAR CONTADOR
    // =====================================================

    function actualizarContador() {


        const transcurrido =
            obtenerTiempoTranscurrido();


        const restante =
            duracionTotal -
            transcurrido;



        if (
            restante <= 0
        ) {


            contador.textContent =
                "00:00";


            if (mensaje) {

                mensaje.textContent =
                    "El tiempo del descanso ha terminado. Pulsa finalizar para registrar la hora.";

            }


            return;

        }



        contador.textContent =
            formatearTiempo(
                restante
            );


        if (mensaje) {

            mensaje.textContent =
                "Descanso en progreso";

        }

    }



    actualizarContador();


    setInterval(
        actualizarContador,
        1000
    );

}



// =========================================================
// CONTADOR DE HORAS EXTRAS
// =========================================================

function iniciarContadorHorasExtras(
    contador
) {


    const inicio =
        (
            contador.dataset.inicio ||
            ""
        ).trim();


    if (!inicio) {

        contador.textContent =
            "00:00:00";

        return;

    }



    // =====================================================
    // CONVERTIR FECHA DE FLASK
    // =====================================================

    let fechaInicio =
        new Date(inicio);


    // Si el navegador no reconoce directamente
    // la fecha, intentamos normalizarla.

    if (
        isNaN(
            fechaInicio.getTime()
        )
    ) {


        const normalizada =
            inicio.replace(
                " ",
                "T"
            );


        fechaInicio =
            new Date(
                normalizada
            );

    }



    if (
        isNaN(
            fechaInicio.getTime()
        )
    ) {


        contador.textContent =
            "00:00:00";

        return;

    }



    // =====================================================
    // ACTUALIZAR
    // =====================================================

    function actualizar() {


        const ahora =
            new Date();


        let diferencia =
            Math.floor(

                (
                    ahora.getTime() -
                    fechaInicio.getTime()
                ) / 1000

            );


        if (
            diferencia < 0
        ) {

            diferencia = 0;

        }



        const horas =
            Math.floor(
                diferencia / 3600
            );


        const minutos =
            Math.floor(

                (
                    diferencia % 3600
                ) / 60

            );


        const segundos =
            diferencia % 60;



        contador.textContent =

            String(
                horas
            ).padStart(
                2,
                "0"
            ) +

            ":" +

            String(
                minutos
            ).padStart(
                2,
                "0"
            ) +

            ":" +

            String(
                segundos
            ).padStart(
                2,
                "0"
            );

    }



    actualizar();


    setInterval(
        actualizar,
        1000
    );

}



// =========================================================
// OBTENER UBICACIÓN DEL USUARIO
// =========================================================

function obtenerUbicacionUsuario() {


    const ubicacionTexto =
        document.getElementById(
            "ubicacion-texto"
        );


    const ubicacionActual =
        document.getElementById(
            "ubicacion-actual"
        );


    const latitudElemento =
        document.getElementById(
            "latitud"
        );


    const longitudElemento =
        document.getElementById(
            "longitud"
        );



    // =====================================================
    // COMPROBAR GEOLOCALIZACIÓN
    // =====================================================

    if (
        !navigator.geolocation
    ) {


        const mensaje =
            "Tu navegador no permite obtener la ubicación.";


        if (
            ubicacionTexto
        ) {

            ubicacionTexto.textContent =
                mensaje;

        }


        if (
            ubicacionActual
        ) {

            ubicacionActual.textContent =
                mensaje;

        }


        return;

    }



    // =====================================================
    // SOLICITAR UBICACIÓN
    // =====================================================

    navigator.geolocation.getCurrentPosition(


        function(position) {


            const latitud =
                position.coords.latitude;


            const longitud =
                position.coords.longitude;



            // =================================================
            // MOSTRAR LATITUD
            // =================================================

            if (
                latitudElemento
            ) {

                latitudElemento.textContent =
                    latitud.toFixed(6);

            }



            // =================================================
            // MOSTRAR LONGITUD
            // =================================================

            if (
                longitudElemento
            ) {

                longitudElemento.textContent =
                    longitud.toFixed(6);

            }



            // =================================================
            // TEXTO DE UBICACIÓN
            // =================================================

            const coordenadas =

                `${latitud.toFixed(6)}, ${longitud.toFixed(6)}`;



            if (
                ubicacionTexto
            ) {

                ubicacionTexto.textContent =
                    coordenadas;

            }


            if (
                ubicacionActual
            ) {

                ubicacionActual.textContent =
                    coordenadas;

            }

        },


        function(error) {


            let mensaje =
                "No se pudo obtener tu ubicación.";



            if (
                error.code ===
                error.PERMISSION_DENIED
            ) {


                mensaje =
                    "Debes permitir el acceso a tu ubicación.";

            }


            else if (
                error.code ===
                error.POSITION_UNAVAILABLE
            ) {


                mensaje =
                    "La ubicación no está disponible.";

            }


            else if (
                error.code ===
                error.TIMEOUT
            ) {


                mensaje =
                    "Se agotó el tiempo para obtener la ubicación.";

            }



            if (
                ubicacionTexto
            ) {

                ubicacionTexto.textContent =
                    mensaje;

            }


            if (
                ubicacionActual
            ) {

                ubicacionActual.textContent =
                    mensaje;

            }


        },


        {

            enableHighAccuracy:
                true,

            timeout:
                10000,

            maximumAge:
                0

        }

    );

}



// =========================================================
// OBTENER UBICACIÓN COMO PROMESA
// =========================================================

function obtenerUbicacion() {


    return new Promise(
        function(resolve, reject) {


            if (
                !navigator.geolocation
            ) {

                reject(
                    new Error(
                        "Tu navegador no permite obtener la ubicación."
                    )
                );

                return;

            }



            navigator.geolocation.getCurrentPosition(


                function(position) {


                    resolve({

                        latitud:
                            position.coords.latitude,

                        longitud:
                            position.coords.longitude,

                        precision:
                            position.coords.accuracy

                    });

                },


                function(error) {


                    let mensaje =
                        "No se pudo obtener tu ubicación.";



                    if (
                        error.code ===
                        error.PERMISSION_DENIED
                    ) {

                        mensaje =
                            "Debes permitir el acceso a tu ubicación para continuar.";

                    }


                    else if (
                        error.code ===
                        error.POSITION_UNAVAILABLE
                    ) {

                        mensaje =
                            "La ubicación no está disponible.";

                    }


                    else if (
                        error.code ===
                        error.TIMEOUT
                    ) {

                        mensaje =
                            "Se agotó el tiempo para obtener la ubicación.";

                    }



                    reject(
                        new Error(
                            mensaje
                        )
                    );

                },


                {

                    enableHighAccuracy:
                        true,

                    timeout:
                        10000,

                    maximumAge:
                        0

                }

            );

        }
    );

}



// =========================================================
// MOSTRAR UBICACIÓN EN LA VISTA
// =========================================================

function mostrarUbicacion(
    ubicacion
) {


    const latitud =
        ubicacion.latitud;


    const longitud =
        ubicacion.longitud;


    const coordenadas =

        `${latitud.toFixed(6)}, ${longitud.toFixed(6)}`;



    const ubicacionTexto =
        document.getElementById(
            "ubicacion-texto"
        );


    const ubicacionActual =
        document.getElementById(
            "ubicacion-actual"
        );


    const latitudElemento =
        document.getElementById(
            "latitud"
        );


    const longitudElemento =
        document.getElementById(
            "longitud"
        );



    if (
        ubicacionTexto
    ) {

        ubicacionTexto.textContent =
            coordenadas;

    }


    if (
        ubicacionActual
    ) {

        ubicacionActual.textContent =
            coordenadas;

    }


    if (
        latitudElemento
    ) {

        latitudElemento.textContent =
            latitud.toFixed(6);

    }


    if (
        longitudElemento
    ) {

        longitudElemento.textContent =
            longitud.toFixed(6);

    }

}



// =========================================================
// OBTENER UBICACIÓN PARA HORAS EXTRAS
// =========================================================

async function obtenerUbicacionParaHorasExtras() {


    try {


        const ubicacion =
            await obtenerUbicacion();


        mostrarUbicacion(
            ubicacion
        );


        return ubicacion;


    }

    catch (error) {


        throw error;

    }

}



// =========================================================
// INICIAR HORAS EXTRAS
// =========================================================

async function iniciarHorasExtras() {


    const boton =
        document.querySelector(
            ".btn-iniciar-horas-extras"
        );


    // =====================================================
    // DESACTIVAR BOTÓN
    // =====================================================

    if (boton) {

        boton.disabled =
            true;


        boton.innerHTML =

            '<i class="bi bi-hourglass-split"></i> OBTENIENDO UBICACIÓN...';

    }



    try {


        // =================================================
        // OBTENER GPS
        // =================================================

        const ubicacion =
            await obtenerUbicacionParaHorasExtras();



        // =================================================
        // COMPROBAR URL
        // =================================================

        if (
            !window.ATTENDIX ||
            !window.ATTENDIX.iniciarHorasExtrasUrl
        ) {


            throw new Error(
                "No se encontró la URL para iniciar horas extras."
            );

        }



        // =================================================
        // ENVIAR AL SERVIDOR
        // =================================================

        const response =
            await fetch(

                window
                    .ATTENDIX
                    .iniciarHorasExtrasUrl,

                {

                    method:
                        "POST",

                    headers: {

                        "Content-Type":
                            "application/json",

                        "Accept":
                            "application/json"

                    },

                    body:
                        JSON.stringify({

                            latitud:
                                ubicacion.latitud,

                            longitud:
                                ubicacion.longitud,

                            precision:
                                ubicacion.precision,

                            ubicacion:

                                `${ubicacion.latitud}, ${ubicacion.longitud}`

                        })

                }

            );



        // =================================================
        // LEER RESPUESTA
        // =================================================

        let data;


        try {

            data =
                await response.json();

        }

        catch {

            data = {};

        }



        // =================================================
        // COMPROBAR RESPUESTA
        // =================================================

        if (
            !response.ok ||
            !data.exito
        ) {


            throw new Error(

                data.mensaje ||

                "No se pudieron iniciar las horas extras."

            );

        }



        // =================================================
        // RECARGAR
        // =================================================

        window.location.reload();


    }

    catch (error) {


        console.error(
            "Error iniciando horas extras:",
            error
        );


        alert(
            error.message
        );



        // =================================================
        // RESTAURAR BOTÓN
        // =================================================

        if (boton) {


            boton.disabled =
                false;


            boton.innerHTML =

                '<i class="bi bi-clock-fill"></i> INICIAR HORAS EXTRAS';

        }

    }

}



// =========================================================
// FINALIZAR HORAS EXTRAS
// =========================================================

async function finalizarHorasExtras() {


    const boton =
        document.querySelector(
            ".btn-finalizar-horas-extras"
        );


    // =====================================================
    // DESACTIVAR BOTÓN
    // =====================================================

    if (boton) {


        boton.disabled =
            true;


        boton.innerHTML =

            '<i class="bi bi-hourglass-split"></i> OBTENIENDO UBICACIÓN...';

    }



    try {


        // =================================================
        // OBTENER GPS
        // =================================================

        const ubicacion =
            await obtenerUbicacionParaHorasExtras();



        // =================================================
        // COMPROBAR URL
        // =================================================

        if (
            !window.ATTENDIX ||
            !window.ATTENDIX.finalizarHorasExtrasUrl
        ) {


            throw new Error(
                "No se encontró la URL para finalizar horas extras."
            );

        }



        // =================================================
        // CAMBIAR TEXTO
        // =================================================

        if (boton) {


            boton.innerHTML =

                '<i class="bi bi-hourglass-split"></i> FINALIZANDO...';

        }



        // =================================================
        // ENVIAR AL SERVIDOR
        // =================================================

        const response =
            await fetch(

                window
                    .ATTENDIX
                    .finalizarHorasExtrasUrl,

                {

                    method:
                        "POST",

                    headers: {

                        "Content-Type":
                            "application/json",

                        "Accept":
                            "application/json"

                    },

                    body:
                        JSON.stringify({

                            latitud:
                                ubicacion.latitud,

                            longitud:
                                ubicacion.longitud,

                            precision:
                                ubicacion.precision,

                            ubicacion:

                                `${ubicacion.latitud}, ${ubicacion.longitud}`

                        })

                }

            );



        // =================================================
        // LEER RESPUESTA
        // =================================================

        let data;


        try {

            data =
                await response.json();

        }

        catch {

            data = {};

        }



        // =================================================
        // COMPROBAR RESPUESTA
        // =================================================

        if (
            !response.ok ||
            !data.exito
        ) {


            throw new Error(

                data.mensaje ||

                "No se pudieron finalizar las horas extras."

            );

        }



        // =================================================
        // RECARGAR
        // =================================================

        window.location.reload();


    }

    catch (error) {


        console.error(
            "Error finalizando horas extras:",
            error
        );


        alert(
            error.message
        );



        // =================================================
        // RESTAURAR BOTÓN
        // =================================================

        if (boton) {


            boton.disabled =
                false;


            boton.innerHTML =

                '<i class="bi bi-stop-circle-fill"></i> FINALIZAR HORAS EXTRAS';

        }

    }

}



// =========================================================
// PREVENIR DOBLE ENVÍO DE FORMULARIOS
// =========================================================

document.addEventListener(
    "submit",
    function(event) {


        const formulario =
            event.target;


        if (
            formulario.id ===
            "form-finalizar-descanso"
        ) {


            const boton =
                formulario.querySelector(
                    "button"
                );


            if (boton) {


                boton.disabled =
                    true;


                boton.innerHTML =

                    '<i class="bi bi-hourglass-split"></i> FINALIZANDO...';

            }

        }

    }
);
