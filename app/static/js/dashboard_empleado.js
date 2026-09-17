// ==========================================
// DASHBOARD EMPLEADO
// CONTADOR DE DESCANSOS
// UBICACIÓN DEL USUARIO
// ==========================================

document.addEventListener("DOMContentLoaded", function () {

    // ==========================================================
    // CONTADOR DE DESCANSOS
    // ==========================================================

    const contador =
        document.getElementById("contador");


    // ==========================================================
    // SI EXISTE UN DESCANSO ACTIVO
    // ==========================================================

    if (contador) {

        const mensaje =
            document.getElementById("mensaje-contador");

        const formulario =
            document.getElementById("form-finalizar-descanso");

        const boton =
            document.getElementById("btn-finalizar-descanso");


        // ======================================================
        // DATOS DEL DESCANSO
        // ======================================================

        const tipoDescanso =
            (contador.dataset.tipo || "").trim();

        const horaInicio =
            (contador.dataset.inicio || "").trim();


        console.log(
            "Tipo de descanso:",
            tipoDescanso
        );

        console.log(
            "Hora de inicio:",
            horaInicio
        );


        // ======================================================
        // DURACIONES
        // ======================================================

        const duraciones = {

            break_manana: 15 * 60,

            lunch: 60 * 60,

            break_tarde: 15 * 60

        };


        const duracionTotal =
            duraciones[tipoDescanso];


        // ======================================================
        // VALIDAR TIPO DE DESCANSO
        // ======================================================

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

        } else {

            // ==================================================
            // CONVERTIR HORA A SEGUNDOS
            // ==================================================

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


            // ==================================================
            // HORA DE INICIO
            // ==================================================

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

            } else {

                // ==================================================
                // OBTENER HORA ACTUAL
                // ==================================================

                function obtenerHoraActualSegundos() {

                    const ahora =
                        new Date();


                    return (
                        ahora.getHours() * 3600 +
                        ahora.getMinutes() * 60 +
                        ahora.getSeconds()
                    );
                }


                // ==================================================
                // TIEMPO TRANSCURRIDO
                // ==================================================

                function obtenerTiempoTranscurrido() {

                    const actual =
                        obtenerHoraActualSegundos();


                    let diferencia =
                        actual -
                        inicioSegundos;


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


                // ==================================================
                // FORMATEAR TIEMPO
                // ==================================================

                function formatearTiempo(
                    segundos
                ) {

                    segundos =
                        Math.max(
                            0,
                            Math.floor(
                                segundos
                            )
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


                // ==================================================
                // ACTUALIZAR CONTADOR
                // ==================================================

                function actualizarContador() {

                    const transcurrido =
                        obtenerTiempoTranscurrido();


                    const restante =
                        duracionTotal -
                        transcurrido;


                    // ==========================================
                    // TIEMPO TERMINADO
                    // ==========================================

                    if (restante <= 0) {

                        contador.textContent =
                            "00:00";


                        if (mensaje) {

                            mensaje.textContent =
                                "El tiempo del descanso ha terminado. Pulsa finalizar para registrar la hora.";

                        }


                        /*
                         * NO finalizamos automáticamente.
                         *
                         * El empleado debe pulsar
                         * el botón de finalizar.
                         */

                        return;
                    }


                    // ==========================================
                    // MOSTRAR TIEMPO
                    // ==========================================

                    contador.textContent =
                        formatearTiempo(
                            restante
                        );


                    if (mensaje) {

                        mensaje.textContent =
                            "Descanso en progreso";

                    }
                }


                // ==================================================
                // PRIMERA EJECUCIÓN
                // ==================================================

                actualizarContador();


                // ==================================================
                // ACTUALIZAR CADA SEGUNDO
                // ==================================================

                const intervalo =
                    setInterval(
                        actualizarContador,
                        1000
                    );


                // ==================================================
                // FINALIZAR MANUALMENTE
                // ==================================================

                if (
                    formulario &&
                    boton
                ) {

                    formulario.addEventListener(
                        "submit",
                        function () {

                            boton.disabled =
                                true;


                            boton.textContent =
                                "FINALIZANDO...";


                            clearInterval(
                                intervalo
                            );
                        }
                    );
                }
            }
        }
    }


    // ==========================================================
    // UBICACIÓN DEL USUARIO
    // ==========================================================

    const ubicacionTexto =
        document.getElementById(
            "ubicacion-texto"
        );


    // Si el elemento no existe,
    // no hacemos nada.

    if (!ubicacionTexto) {
        return;
    }


    // ==========================================================
    // MOSTRAR ESTADO
    // ==========================================================

    function mostrarEstadoUbicacion(
        mensaje
    ) {

        ubicacionTexto.textContent =
            mensaje;
    }


    // ==========================================================
    // CREAR DIRECCIÓN CORTA
    // ==========================================================

    function construirDireccionCorta(
        datos
    ) {

        const address =
            datos.address || {};


        const partes = [];


        // ======================================================
        // NOMBRE DEL LUGAR
        // ======================================================

        const lugar =
            datos.name ||
            address.amenity ||
            address.shop ||
            address.tourism ||
            address.hotel ||
            address.building;


        if (lugar) {

            partes.push(lugar);

        }


        // ======================================================
        // CALLE + NÚMERO
        // ======================================================

        if (address.road) {

            let calle =
                address.road;


            if (address.house_number) {

                calle +=
                    ` ${address.house_number}`;

            }


            partes.push(
                calle
            );
        }


        // ======================================================
        // BARRIO / ZONA
        // ======================================================

        const zona =
            address.neighbourhood ||
            address.suburb ||
            address.quarter ||
            address.city_district;


        if (zona) {

            partes.push(
                zona
            );
        }


        // ======================================================
        // CIUDAD
        // ======================================================

        const ciudad =
            address.city ||
            address.town ||
            address.village ||
            address.municipality;


        if (ciudad) {

            partes.push(
                ciudad
            );
        }


        // ======================================================
        // ESTADO / PROVINCIA / DEPARTAMENTO
        // ======================================================

        const estado =
            address.state ||
            address.province ||
            address.region;


        if (estado) {

            partes.push(
                estado
            );
        }


        // ======================================================
        // PAÍS
        // ======================================================

        if (address.country) {

            partes.push(
                address.country
            );
        }


        // ======================================================
        // ELIMINAR DUPLICADOS
        // ======================================================

        const resultado =
            [...new Set(partes)];


        return resultado.join(
            ", "
        );
    }


    // ==========================================================
    // OBTENER UBICACIÓN
    // ==========================================================

    function obtenerUbicacion() {

        return new Promise(
            function (
                resolve,
                reject
            ) {

                if (
                    !navigator.geolocation
                ) {

                    reject(
                        new Error(
                            "Este navegador no soporta la geolocalización."
                        )
                    );

                    return;
                }


                navigator.geolocation.getCurrentPosition(

                    // ==================================================
                    // ÉXITO
                    // ==================================================

                    function (
                        position
                    ) {

                        resolve({

                            latitud:
                                position.coords.latitude,

                            longitud:
                                position.coords.longitude

                        });
                    },


                    // ==================================================
                    // ERROR
                    // ==================================================

                    function (
                        error
                    ) {

                        switch (
                            error.code
                        ) {

                            case error.PERMISSION_DENIED:

                                reject(
                                    new Error(
                                        "Permiso de ubicación denegado."
                                    )
                                );

                                break;


                            case error.POSITION_UNAVAILABLE:

                                reject(
                                    new Error(
                                        "La ubicación no está disponible."
                                    )
                                );

                                break;


                            case error.TIMEOUT:

                                reject(
                                    new Error(
                                        "Se agotó el tiempo para obtener la ubicación."
                                    )
                                );

                                break;


                            default:

                                reject(
                                    new Error(
                                        "No se pudo obtener la ubicación."
                                    )
                                );
                        }
                    },


                    // ==================================================
                    // OPCIONES
                    // ==================================================

                    {

                        enableHighAccuracy:
                            true,

                        timeout:
                            15000,

                        maximumAge:
                            300000

                    }
                );
            }
        );
    }


    // ==========================================================
    // OBTENER DIRECCIÓN
    // ==========================================================

    async function obtenerDireccion(
        latitud,
        longitud
    ) {

        const url =
            "https://nominatim.openstreetmap.org/reverse" +
            "?format=jsonv2" +
            "&lat=" +
            encodeURIComponent(
                latitud
            ) +
            "&lon=" +
            encodeURIComponent(
                longitud
            ) +
            "&zoom=18" +
            "&addressdetails=1";


        const respuesta =
            await fetch(
                url,
                {

                    headers: {

                        Accept:
                            "application/json"

                    }

                }
            );


        if (!respuesta.ok) {

            throw new Error(
                "No se pudo obtener la dirección."
            );
        }


        return await respuesta.json();
    }


    // ==========================================================
    // CARGAR UBICACIÓN
    // ==========================================================

    async function cargarUbicacion() {

        mostrarEstadoUbicacion(
            "Obteniendo ubicación..."
        );


        try {

            // ==================================================
            // COORDENADAS
            // ==================================================

            const ubicacion =
                await obtenerUbicacion();


            const latitud =
                ubicacion.latitud;


            const longitud =
                ubicacion.longitud;


            console.log(
                "Latitud:",
                latitud
            );


            console.log(
                "Longitud:",
                longitud
            );


            // ==================================================
            // DIRECCIÓN
            // ==================================================

            const datos =
                await obtenerDireccion(
                    latitud,
                    longitud
                );


            console.log(
                "Datos de ubicación:",
                datos
            );


            // ==================================================
            // DIRECCIÓN CORTA
            // ==================================================

            const direccionCorta =
                construirDireccionCorta(
                    datos
                );


            // ==================================================
            // MOSTRAR DIRECCIÓN
            // ==================================================

            if (direccionCorta) {

                ubicacionTexto.textContent =
                    direccionCorta;

            } else {

                ubicacionTexto.textContent =
                    `${latitud.toFixed(5)}, ${longitud.toFixed(5)}`;
            }


        } catch (error) {

            console.error(
                "Error obteniendo ubicación:",
                error
            );


            mostrarEstadoUbicacion(
                "Ubicación no disponible"
            );
        }
    }


    // ==========================================================
    // INICIAR UBICACIÓN
    // ==========================================================

    cargarUbicacion();

});



// ==========================================================
    // HORAS EXTRAS     
    // ==========================================================
document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById(
        "form-iniciar-hora-extra"
    );

    const button = document.getElementById(
        "btn-iniciar-hora-extra"
    );

    const latitudInput = document.getElementById(
        "hora-extra-latitud"
    );

    const longitudInput = document.getElementById(
        "hora-extra-longitud"
    );

    const direccionInput = document.getElementById(
        "hora-extra-direccion"
    );


    form.addEventListener("submit", function (event) {

        // Evitar que el formulario se envíe inmediatamente
        event.preventDefault();


        // -------------------------------------------------
        // Verificar soporte de geolocalización
        // -------------------------------------------------

        if (!navigator.geolocation) {

            alert(
                "Tu navegador no permite obtener la ubicación."
            );

            return;
        }


        // -------------------------------------------------
        // Deshabilitar botón mientras obtenemos ubicación
        // -------------------------------------------------

        button.disabled = true;

        const textoOriginal = button.innerHTML;

        button.innerHTML = `
            <div class="break-option-icon">
                <i class="bi bi-geo-alt-fill"></i>
            </div>

            <div class="break-option-info">
                <strong>
                    Obteniendo ubicación...
                </strong>

                <small>
                    Espera un momento
                </small>
            </div>
        `;


        // -------------------------------------------------
        // Obtener ubicación
        // -------------------------------------------------

        navigator.geolocation.getCurrentPosition(

            function (position) {

                const latitud =
                    position.coords.latitude;

                const longitud =
                    position.coords.longitude;


                // -----------------------------------------
                // Guardar coordenadas en el formulario
                // -----------------------------------------

                latitudInput.value = latitud;

                longitudInput.value = longitud;


                // -----------------------------------------
                // Por ahora no tenemos geocodificación
                // -----------------------------------------

                direccionInput.value = "";


                // -----------------------------------------
                // Enviar formulario
                // -----------------------------------------

                form.submit();

            },


            function (error) {

                button.disabled = false;

                button.innerHTML = textoOriginal;


                let mensaje =
                    "No fue posible obtener tu ubicación.";


                switch (error.code) {

                    case error.PERMISSION_DENIED:

                        mensaje =
                            "Debes permitir el acceso a tu ubicación para iniciar las horas extras.";

                        break;


                    case error.POSITION_UNAVAILABLE:

                        mensaje =
                            "No se pudo determinar tu ubicación.";

                        break;


                    case error.TIMEOUT:

                        mensaje =
                            "La solicitud de ubicación tardó demasiado.";

                        break;
                }


                alert(mensaje);
            },


            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }

        );

    });

});

