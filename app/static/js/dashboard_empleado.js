// ==========================================
// DASHBOARD EMPLEADO
// CONTADOR DE DESCANSOS
// UBICACIÓN
// HORAS EXTRAS
// ==========================================

document.addEventListener("DOMContentLoaded", function () {

    // ==========================================================
    // CONTADOR DE DESCANSOS
    // ==========================================================

    const contador =
        document.getElementById("contador");


    if (contador) {

        const mensaje =
            document.getElementById("mensaje-contador");

        const formulario =
            document.getElementById("form-finalizar-descanso");

        const boton =
            document.getElementById("btn-finalizar-descanso");


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


        const duraciones = {

            break_manana: 15 * 60,

            lunch: 60 * 60,

            break_tarde: 15 * 60

        };


        const duracionTotal =
            duraciones[tipoDescanso];


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

                function obtenerHoraActualSegundos() {

                    const ahora =
                        new Date();


                    return (
                        ahora.getHours() * 3600 +
                        ahora.getMinutes() * 60 +
                        ahora.getSeconds()
                    );
                }


                function obtenerTiempoTranscurrido() {

                    const actual =
                        obtenerHoraActualSegundos();


                    let diferencia =
                        actual -
                        inicioSegundos;


                    if (diferencia < 0) {

                        diferencia +=
                            24 * 60 * 60;

                    }


                    return diferencia;
                }


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


                const intervalo =
                    setInterval(
                        actualizarContador,
                        1000
                    );


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
    // ELEMENTOS DE UBICACIÓN
    // ==========================================================

    const ubicacionTexto =
        document.getElementById(
            "ubicacion-texto"
        );


    const formHoraExtra =
        document.getElementById(
            "form-iniciar-hora-extra"
        );


    const botonHoraExtra =
        document.getElementById(
            "btn-iniciar-hora-extra"
        );


    const latitudInput =
        document.getElementById(
            "hora-extra-latitud"
        );


    const longitudInput =
        document.getElementById(
            "hora-extra-longitud"
        );


    const direccionInput =
        document.getElementById(
            "hora-extra-direccion"
        );


    // ==========================================================
    // CREAR DIRECCIÓN CORTA
    // ==========================================================

    function construirDireccionCorta(
        datos
    ) {

        const address =
            datos.address || {};


        const partes = [];


        // ------------------------------------------------------
        // NOMBRE DEL LUGAR
        // ------------------------------------------------------

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


        // ------------------------------------------------------
        // CALLE + NÚMERO
        // ------------------------------------------------------

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


        // ------------------------------------------------------
        // BARRIO / ZONA
        // ------------------------------------------------------

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


        // ------------------------------------------------------
        // CIUDAD
        // ------------------------------------------------------

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


        // ------------------------------------------------------
        // DEPARTAMENTO
        // ------------------------------------------------------

        const estado =
            address.state ||
            address.province ||
            address.region;


        if (estado) {

            partes.push(
                estado
            );
        }


        // ------------------------------------------------------
        // PAÍS
        // ------------------------------------------------------

        if (address.country) {

            partes.push(
                address.country
            );
        }


        // ------------------------------------------------------
        // ELIMINAR DUPLICADOS
        // ------------------------------------------------------

        return [
            ...new Set(partes)
        ].join(", ");
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

                    function (position) {

                        resolve({

                            latitud:
                                position.coords.latitude,

                            longitud:
                                position.coords.longitude

                        });

                    },


                    function (error) {

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
    // OBTENER DIRECCIÓN DESDE COORDENADAS
    // ==========================================================

    async function obtenerDireccion(
        latitud,
        longitud
    ) {

        const url =
            "https://nominatim.openstreetmap.org/reverse" +
            "?format=jsonv2" +
            "&lat=" +
            encodeURIComponent(latitud) +
            "&lon=" +
            encodeURIComponent(longitud) +
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
    // OBTENER UBICACIÓN PARA EL DASHBOARD
    // ==========================================================

    async function cargarUbicacion() {

        if (!ubicacionTexto) {
            return;
        }


        ubicacionTexto.textContent =
            "Obteniendo ubicación...";


        try {

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


            try {

                const datos =
                    await obtenerDireccion(
                        latitud,
                        longitud
                    );


                console.log(
                    "Datos de ubicación:",
                    datos
                );


                const direccion =
                    construirDireccionCorta(
                        datos
                    );


                if (direccion) {

                    ubicacionTexto.textContent =
                        direccion;

                } else {

                    ubicacionTexto.textContent =
                        `${latitud.toFixed(5)}, ${longitud.toFixed(5)}`;

                }

            } catch (errorDireccion) {

                console.error(
                    "Error obteniendo dirección:",
                    errorDireccion
                );


                ubicacionTexto.textContent =
                    `${latitud.toFixed(5)}, ${longitud.toFixed(5)}`;
            }


        } catch (error) {

            console.error(
                "Error obteniendo ubicación:",
                error
            );


            ubicacionTexto.textContent =
                "Ubicación no disponible";
        }
    }


    // ==========================================================
    // INICIAR HORA EXTRA
    // ==========================================================

    if (
        formHoraExtra &&
        botonHoraExtra &&
        latitudInput &&
        longitudInput &&
        direccionInput
    ) {

        formHoraExtra.addEventListener(
            "submit",
            async function (event) {

                // ----------------------------------------------
                // Evitar envío inmediato
                // ----------------------------------------------

                event.preventDefault();


                // ----------------------------------------------
                // Guardar HTML original
                // ----------------------------------------------

                const textoOriginal =
                    botonHoraExtra.innerHTML;


                // ----------------------------------------------
                // Deshabilitar botón
                // ----------------------------------------------

                botonHoraExtra.disabled =
                    true;


                botonHoraExtra.innerHTML = `
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


                try {

                    // ==========================================
                    // 1. OBTENER GPS
                    // ==========================================

                    const ubicacion =
                        await obtenerUbicacion();


                    const latitud =
                        ubicacion.latitud;


                    const longitud =
                        ubicacion.longitud;


                    console.log(
                        "Hora extra - latitud:",
                        latitud
                    );


                    console.log(
                        "Hora extra - longitud:",
                        longitud
                    );


                    // ==========================================
                    // 2. GUARDAR COORDENADAS
                    // ==========================================

                    latitudInput.value =
                        latitud;


                    longitudInput.value =
                        longitud;


                    // ==========================================
                    // 3. OBTENER DIRECCIÓN
                    // ==========================================

                    botonHoraExtra.innerHTML = `
                        <div class="break-option-icon">
                            <i class="bi bi-map-fill"></i>
                        </div>

                        <div class="break-option-info">
                            <strong>
                                Obteniendo dirección...
                            </strong>

                            <small>
                                Espera un momento
                            </small>
                        </div>
                    `;


                    try {

                        const datos =
                            await obtenerDireccion(
                                latitud,
                                longitud
                            );


                        const direccion =
                            construirDireccionCorta(
                                datos
                            );


                        direccionInput.value =
                            direccion || "";


                        console.log(
                            "Hora extra - dirección:",
                            direccion
                        );

                    } catch (errorDireccion) {

                        console.error(
                            "No se pudo obtener la dirección:",
                            errorDireccion
                        );


                        // ------------------------------------------------
                        // Si falla la dirección, conservamos las coordenadas
                        // ------------------------------------------------

                        direccionInput.value =
                            "";
                    }


                    // ==========================================
                    // 4. ENVIAR FORMULARIO
                    // ==========================================

                    botonHoraExtra.innerHTML = `
                        <div class="break-option-icon">
                            <i class="bi bi-check-circle-fill"></i>
                        </div>

                        <div class="break-option-info">
                            <strong>
                                Registrando...
                            </strong>

                            <small>
                                Guardando hora extra
                            </small>
                        </div>
                    `;


                    formHoraExtra.submit();


                } catch (error) {

                    console.error(
                        "Error obteniendo ubicación:",
                        error
                    );


                    // ------------------------------------------
                    // Restaurar botón
                    // ------------------------------------------

                    botonHoraExtra.disabled =
                        false;


                    botonHoraExtra.innerHTML =
                        textoOriginal;


                    alert(
                        error.message ||
                        "No fue posible obtener tu ubicación."
                    );
                }

            }
        );
    }


    // ==========================================================
    // CARGAR UBICACIÓN DEL DASHBOARD
    // ==========================================================

    cargarUbicacion();

});

document.addEventListener(
    "DOMContentLoaded",
    function () {
        const mensajes = document.querySelectorAll(".custom-toast");
        mensajes.forEach(function (mensaje) {
            setTimeout(function () {
                mensaje.style.transition = "opacity 0.4s ease, transform 0.4s ease";
                mensaje.style.opacity = "0";
                mensaje.style.transform = "translateY(-10px)";
                setTimeout(function () {
                    mensaje.remove();
                }, 400);
            }, 4000);
        });
    }
);

// =====================================================
// COMPROBAR ESTADO DE LA CUENTA 
// =====================================================

setInterval(async function () {

    try {

        const response = await fetch(
            "{{ url_for('auth.check_session') }}",
            {
                method: "GET",
                credentials: "same-origin",
                cache: "no-store"
            }
        );

        const data = await response.json();

        console.log("Estado de sesión:", data);


        // =================================================
        // CUENTA DESACTIVADA
        // activo = 0
        // =================================================

        if (
            data.motivo === "cuenta_desactivada"
        ) {

            // Evitar que la modal se cree varias veces
            if (
                document.getElementById(
                    "cuenta-desactivada-modal"
                )
            ) {
                return;
            }


            // Crear modal
            const modal = document.createElement("div");

            modal.id = "cuenta-desactivada-modal";


            modal.innerHTML = `
                <div style="
                    position: fixed;
                    inset: 0;
                    background: rgba(15, 23, 42, 0.75);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 999999;
                ">

                    <div style="
                        background: #ffffff;
                        width: min(420px, 90%);
                        border-radius: 20px;
                        padding: 32px;
                        text-align: center;
                        box-shadow: 0 20px 50px rgba(0,0,0,.25);
                    ">

                        <div style="
                            width: 65px;
                            height: 65px;
                            margin: 0 auto 20px;
                            border-radius: 50%;
                            background: #fee2e2;
                            color: #dc2626;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-size: 28px;
                        ">

                            <i class="bi bi-person-x-fill"></i>

                        </div>


                        <h3 style="
                            margin: 0 0 10px;
                            color: #1e293b;
                        ">
                            Cuenta desactivada
                        </h3>


                        <p style="
                            color: #64748b;
                            margin: 0 0 25px;
                            line-height: 1.5;
                        ">
                            Tu cuenta ha sido desactivada por un
                            administrador. Tu sesión se cerrará.
                        </p>


                        <button
                            id="btn-cerrar-sesion-desactivado"
                            type="button"
                            style="
                                border: 0;
                                background: #dc2626;
                                color: white;
                                padding: 11px 25px;
                                border-radius: 10px;
                                font-weight: 600;
                                cursor: pointer;
                            "
                        >
                            Ir al inicio de sesión
                        </button>

                    </div>

                </div>
            `;


            document.body.appendChild(modal);


            // =================================================
            // BOTÓN PARA CERRAR SESIÓN
            // =================================================

            document
                .getElementById(
                    "btn-cerrar-sesion-desactivado"
                )
                .addEventListener(
                    "click",
                    function () {

                        // Ir a la ruta de logout
                        window.location.href =
                            "{{ url_for('auth.logout') }}";

                    }
                );


            // =================================================
            // BLOQUEAR SCROLL
            // =================================================

            document.body.style.overflow = "hidden";
        }


    } catch (error) {

        console.error(
            "Error comprobando la sesión:",
            error
        );

    }

}, 10000);
