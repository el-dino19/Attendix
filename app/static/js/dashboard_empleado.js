// =========================================================
// DASHBOARD EMPLEADO - ATTENDIX
// =========================================================


// =========================================================
// CONFIGURACIÓN DE RUTAS FLASK
// =========================================================
//
// Estas URLs son generadas directamente desde Flask.
// Así evitamos depender de URLs escritas manualmente.
//
// IMPORTANTE:
// Este bloque debe estar disponible ANTES de ejecutar
// iniciarHorasExtras() o finalizarHorasExtras().
//
// =========================================================

window.ATTENDIX = {

    iniciarHorasExtrasUrl:
        "/Attendix/horas-extras/iniciar",

    finalizarHorasExtrasUrl:
        "/Attendix/horas-extras/finalizar",

    estadoHorasExtrasUrl:
        "/Attendix/horas-extras/estado"

};


// =========================================================
// INICIO DEL DASHBOARD
// =========================================================

document.addEventListener("DOMContentLoaded", function () {

    // =====================================================
    // RELOJ DIGITAL
    // =====================================================

    actualizarReloj();

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

                if (mensaje) {
                    mensaje.remove();
                }

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
    // UBICACIÓN
    // =====================================================

    obtenerUbicacionUsuario();

});


// =========================================================
// RELOJ DIGITAL
// =========================================================

function actualizarReloj() {

    const reloj =
        document.getElementById(
            "reloj"
        );

    const fecha =
        document.getElementById(
            "fecha-actual"
        );


    if (!reloj) {
        return;
    }


    const ahora =
        new Date();


    const opcionesHora = {

        timeZone:
            "America/Bogota",

        hour:
            "2-digit",

        minute:
            "2-digit",

        second:
            "2-digit",

        hour12:
            true

    };


    const opcionesFecha = {

        timeZone:
            "America/Bogota",

        weekday:
            "long",

        year:
            "numeric",

        month:
            "long",

        day:
            "numeric"

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
            fechaColombia
                .charAt(0)
                .toUpperCase() +
            fechaColombia.slice(1);

    }

}


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


    // -----------------------------------------------------
    // Convertir HH:MM:SS a segundos
    // -----------------------------------------------------

    function convertirHoraASegundos(
        hora
    ) {

        const partes =
            hora.split(":");


        if (partes.length !== 3) {
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


    if (inicioSegundos === null) {

        contador.textContent =
            "00:00";


        if (mensaje) {

            mensaje.textContent =
                "No se pudo calcular el tiempo.";

        }

        return;
    }


    // -----------------------------------------------------
    // Hora actual Colombia
    // -----------------------------------------------------

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


        partes.forEach(function (parte) {

            if (parte.type === "hour") {

                horas =
                    Number(
                        parte.value
                    );

            }


            if (parte.type === "minute") {

                minutos =
                    Number(
                        parte.value
                    );

            }


            if (parte.type === "second") {

                segundos =
                    Number(
                        parte.value
                    );

            }

        });


        return (
            horas * 3600 +
            minutos * 60 +
            segundos
        );

    }


    // -----------------------------------------------------
    // Tiempo transcurrido
    // -----------------------------------------------------

    function obtenerTiempoTranscurrido() {

        const actual =
            obtenerHoraActualSegundos();


        let diferencia =
            actual -
            inicioSegundos;


        // Si cambia de día

        if (diferencia < 0) {

            diferencia +=
                24 * 60 * 60;

        }


        return diferencia;

    }


    // -----------------------------------------------------
    // Formatear MM:SS
    // -----------------------------------------------------

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
            ).padStart(
                2,
                "0"
            )

            +

            ":"

            +

            String(
                segundosRestantes
            ).padStart(
                2,
                "0"
            )

        );

    }


    // -----------------------------------------------------
    // Actualizar contador
    // -----------------------------------------------------

    function actualizarContador() {

        const transcurrido =
            obtenerTiempoTranscurrido();


        const restante =
            duracionTotal -
            transcurrido;


        if (restante <= 0) {

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


    let fechaInicio =
        new Date(inicio);


    // -----------------------------------------------------
    // Compatibilidad con fechas sin T
    // -----------------------------------------------------

    if (
        Number.isNaN(
            fechaInicio.getTime()
        )
    ) {

        fechaInicio =
            new Date(
                inicio.replace(
                    " ",
                    "T"
                )
            );

    }


    if (
        Number.isNaN(
            fechaInicio.getTime()
        )
    ) {

        contador.textContent =
            "00:00:00";

        return;

    }


    // -----------------------------------------------------
    // Actualizar
    // -----------------------------------------------------

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


        if (diferencia < 0) {

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
            )

            +

            ":"

            +

            String(
                minutos
            ).padStart(
                2,
                "0"
            )

            +

            ":"

            +

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


    if (!navigator.geolocation) {

        mostrarMensajeUbicacion(
            "Tu navegador no permite obtener la ubicación.",
            true
        );

        return;

    }


    if (ubicacionTexto) {

        ubicacionTexto.textContent =
            "Obteniendo ubicación aproximada...";

    }


    navigator.geolocation.getCurrentPosition(

        async function (position) {

            const latitud =
                position.coords.latitude;


            const longitud =
                position.coords.longitude;


            try {

                const direccion =
                    await obtenerDireccionAproximada(
                        latitud,
                        longitud
                    );


                mostrarDireccion(
                    direccion
                );

            }

            catch (error) {

                console.warn(
                    "No se pudo obtener la dirección:",
                    error
                );


                mostrarDireccion(
                    "Ubicación disponible"
                );

            }

        },


        function (error) {

            manejarErrorUbicacion(
                error
            );

        },


        {

            enableHighAccuracy:
                true,

            timeout:
                10000,

            maximumAge:
                60000

        }

    );

}


// =========================================================
// OBTENER DIRECCIÓN APROXIMADA
// =========================================================

async function obtenerDireccionAproximada(
    latitud,
    longitud
) {

    const url =
        "https://nominatim.openstreetmap.org/reverse" +

        "?format=json" +

        "&lat=" +
        encodeURIComponent(
            latitud
        ) +

        "&lon=" +
        encodeURIComponent(
            longitud
        ) +

        "&zoom=18" +

        "&addressdetails=1" +

        "&accept-language=es";


    const response =
        await fetch(
            url,
            {

                method:
                    "GET",

                headers: {

                    "Accept":
                        "application/json"

                }

            }
        );


    if (!response.ok) {

        throw new Error(
            "No se pudo obtener la dirección."
        );

    }


    const data =
        await response.json();


    if (
        !data ||
        !data.address
    ) {

        throw new Error(
            "No se encontró una dirección."
        );

    }


    const address =
        data.address;


    const calle =
        address.road ||
        address.pedestrian ||
        address.footway ||
        address.residential ||
        "";


    const numero =
        address.house_number ||
        "";


    const barrio =
        address.neighbourhood ||
        address.suburb ||
        address.quarter ||
        "";


    const localidad =
        address.city ||
        address.town ||
        address.village ||
        address.municipality ||
        "";


    const departamento =
        address.state ||
        "";


    const partes = [];


    if (calle) {

        if (numero) {

            partes.push(
                `${calle} ${numero}`
            );

        }

        else {

            partes.push(
                calle
            );

        }

    }


    if (barrio) {

        partes.push(
            barrio
        );

    }


    if (localidad) {

        partes.push(
            localidad
        );

    }


    if (partes.length > 0) {

        return partes.join(
            ", "
        );

    }


    const alternativa = [

        barrio,
        localidad,
        departamento

    ]
        .filter(Boolean)
        .join(", ");


    if (alternativa) {

        return alternativa;

    }


    if (data.display_name) {

        const nombre =
            data.display_name
                .split(",")
                .slice(0, 3)
                .join(",");


        if (nombre.trim()) {

            return nombre.trim();

        }

    }


    return "Ubicación aproximada disponible";

}


// =========================================================
// MOSTRAR DIRECCIÓN
// =========================================================

function mostrarDireccion(
    direccion
) {

    const ubicacionTexto =
        document.getElementById(
            "ubicacion-texto"
        );


    const ubicacionActual =
        document.getElementById(
            "ubicacion-actual"
        );


    if (ubicacionTexto) {

        ubicacionTexto.textContent =
            direccion;

    }


    if (ubicacionActual) {

        ubicacionActual.textContent =
            direccion;

    }


    const coordenadas =
        document.querySelector(
            ".ubicacion-coordenadas"
        );


    if (coordenadas) {

        coordenadas.style.display =
            "none";

    }

}


// =========================================================
// MENSAJE DE UBICACIÓN
// =========================================================

function mostrarMensajeUbicacion(
    mensaje,
    ocultarCoordenadas = true
) {

    const ubicacionTexto =
        document.getElementById(
            "ubicacion-texto"
        );


    const ubicacionActual =
        document.getElementById(
            "ubicacion-actual"
        );


    if (ubicacionTexto) {

        ubicacionTexto.textContent =
            mensaje;

    }


    if (ubicacionActual) {

        ubicacionActual.textContent =
            mensaje;

    }


    if (ocultarCoordenadas) {

        const coordenadas =
            document.querySelector(
                ".ubicacion-coordenadas"
            );


        if (coordenadas) {

            coordenadas.style.display =
                "none";

        }

    }

}


// =========================================================
// ERROR DE UBICACIÓN
// =========================================================

function manejarErrorUbicacion(
    error
) {

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


    mostrarMensajeUbicacion(
        mensaje
    );

}


// =========================================================
// OBTENER UBICACIÓN COMO PROMESA
// =========================================================

function obtenerUbicacion() {

    return new Promise(
        function (
            resolve,
            reject
        ) {

            if (!navigator.geolocation) {

                reject(
                    new Error(
                        "Tu navegador no permite obtener la ubicación."
                    )
                );

                return;

            }


            navigator.geolocation.getCurrentPosition(

                function (position) {

                    resolve({

                        latitud:
                            position.coords.latitude,

                        longitud:
                            position.coords.longitude,

                        precision:
                            position.coords.accuracy

                    });

                },


                function (error) {

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
                        60000

                }

            );

        }
    );

}


// =========================================================
// OBTENER UBICACIÓN PARA HORAS EXTRAS
// =========================================================

async function obtenerUbicacionParaHorasExtras() {

    const ubicacion =
        await obtenerUbicacion();


    // Mostrar dirección en la interfaz.
    //
    // Las coordenadas siguen siendo privadas
    // y únicamente se envían al backend.

    mostrarUbicacion(
        ubicacion
    );


    return ubicacion;

}


// =========================================================
// MOSTRAR UBICACIÓN
// =========================================================

async function mostrarUbicacion(
    ubicacion
) {

    if (
        !ubicacion ||
        typeof ubicacion.latitud !== "number" ||
        typeof ubicacion.longitud !== "number"
    ) {

        mostrarMensajeUbicacion(
            "Ubicación no disponible."
        );

        return;

    }


    try {

        const direccion =
            await obtenerDireccionAproximada(

                ubicacion.latitud,
                ubicacion.longitud

            );


        mostrarDireccion(
            direccion
        );

    }


    catch (error) {

        console.warn(
            "Error obteniendo dirección:",
            error
        );


        mostrarDireccion(
            "Ubicación aproximada disponible"
        );

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


    if (boton) {

        boton.disabled =
            true;


        boton.innerHTML =
            '<i class="bi bi-hourglass-split"></i> OBTENIENDO UBICACIÓN...';

    }


    try {

        // -------------------------------------------------
        // OBTENER GPS
        // -------------------------------------------------

        const ubicacion =
            await obtenerUbicacionParaHorasExtras();


        // -------------------------------------------------
        // VERIFICAR URL
        // -------------------------------------------------

        if (
            !window.ATTENDIX ||
            !window.ATTENDIX.iniciarHorasExtrasUrl
        ) {

            throw new Error(
                "No se encontró la URL para iniciar horas extras."
            );

        }


        if (boton) {

            boton.innerHTML =
                '<i class="bi bi-hourglass-split"></i> REGISTRANDO...';

        }


        // -------------------------------------------------
        // ENVIAR AL BACKEND
        // -------------------------------------------------

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

                            /*
                             * Por compatibilidad con tu servicio.
                             *
                             * El backend recibe las coordenadas
                             * reales aquí.
                             */

                            ubicacion:
                                `${ubicacion.latitud}, ${ubicacion.longitud}`

                        })

                }

            );


        let data = {};


        try {

            data =
                await response.json();

        }

        catch (error) {

            console.warn(
                "La respuesta no contiene JSON válido."
            );

        }


        if (
            !response.ok ||
            !data.exito
        ) {

            throw new Error(

                data.mensaje ||
                "No se pudieron iniciar las horas extras."

            );

        }


        // -------------------------------------------------
        // ÉXITO
        // -------------------------------------------------

        window.location.reload();

    }


    catch (error) {

        console.error(
            "Error iniciando horas extras:",
            error
        );


        alert(
            error.message ||
            "No se pudieron iniciar las horas extras."
        );


        if (boton) {

            boton.disabled =
                false;


            boton.innerHTML =
                '<i class="bi bi-play-circle-fill"></i> Iniciar horas extras';

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


    if (boton) {

        boton.disabled =
            true;


        boton.innerHTML =
            '<i class="bi bi-hourglass-split"></i> OBTENIENDO UBICACIÓN...';

    }


    try {

        // -------------------------------------------------
        // OBTENER GPS
        // -------------------------------------------------

        const ubicacion =
            await obtenerUbicacionParaHorasExtras();


        // -------------------------------------------------
        // VERIFICAR URL
        // -------------------------------------------------

        if (
            !window.ATTENDIX ||
            !window.ATTENDIX.finalizarHorasExtrasUrl
        ) {

            throw new Error(
                "No se encontró la URL para finalizar horas extras."
            );

        }


        if (boton) {

            boton.innerHTML =
                '<i class="bi bi-hourglass-split"></i> FINALIZANDO...';

        }


        // -------------------------------------------------
        // ENVIAR AL BACKEND
        // -------------------------------------------------

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


        let data = {};


        try {

            data =
                await response.json();

        }

        catch (error) {

            console.warn(
                "La respuesta no contiene JSON válido."
            );

        }


        if (
            !response.ok ||
            !data.exito
        ) {

            throw new Error(

                data.mensaje ||
                "No se pudieron finalizar las horas extras."

            );

        }


        // -------------------------------------------------
        // ÉXITO
        // -------------------------------------------------

        window.location.reload();

    }


    catch (error) {

        console.error(
            "Error finalizando horas extras:",
            error
        );


        alert(
            error.message ||
            "No se pudieron finalizar las horas extras."
        );


        if (boton) {

            boton.disabled =
                false;


            boton.innerHTML =
                '<i class="bi bi-stop-circle-fill"></i> Finalizar horas extras';

        }

    }

}


// =========================================================
// PREVENIR DOBLE ENVÍO DE FORMULARIOS
// =========================================================

document.addEventListener(
    "submit",
    function (event) {

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
