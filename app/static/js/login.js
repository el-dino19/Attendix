document.addEventListener("DOMContentLoaded", function () {

    // =====================================================
    // ELEMENTOS DEL DOM
    // =====================================================

    const formulario = document.getElementById("loginForm");

    const boton = document.getElementById("loginButton");

    const textoBoton = document.getElementById("loginButtonText");

    const iconoBoton = document.getElementById("loginButtonIcon");

    const estado = document.getElementById("estado-ubicacion");

    const passwordInput = document.getElementById("password");

    const togglePassword = document.getElementById("togglePassword");

    const passwordIcon = document.getElementById("passwordIcon");

    const zonaHoraria = document.getElementById("zona_horaria");

    const latitud = document.getElementById("latitud");

    const longitud = document.getElementById("longitud");

    const direccion = document.getElementById("direccion");


    // =====================================================
    // ZONA HORARIA
    // =====================================================

    if (zonaHoraria) {

        try {

            const zona =
                Intl.DateTimeFormat()
                    .resolvedOptions()
                    .timeZone;

            zonaHoraria.value = zona || "UTC";

        } catch (error) {

            console.warn(
                "No se pudo detectar la zona horaria:",
                error
            );

            zonaHoraria.value = "UTC";
        }
    }


    // =====================================================
    // MOSTRAR / OCULTAR CONTRASEÑA
    // =====================================================

    if (
        passwordInput &&
        togglePassword &&
        passwordIcon
    ) {

        togglePassword.addEventListener(
            "click",
            function () {

                if (
                    passwordInput.type === "password"
                ) {

                    passwordInput.type = "text";

                    passwordIcon.classList.remove(
                        "bi-eye"
                    );

                    passwordIcon.classList.add(
                        "bi-eye-slash"
                    );

                    togglePassword.setAttribute(
                        "aria-label",
                        "Ocultar contraseña"
                    );

                } else {

                    passwordInput.type = "password";

                    passwordIcon.classList.remove(
                        "bi-eye-slash"
                    );

                    passwordIcon.classList.add(
                        "bi-eye"
                    );

                    togglePassword.setAttribute(
                        "aria-label",
                        "Mostrar contraseña"
                    );
                }

            }
        );
    }


    // =====================================================
    // MOSTRAR ESTADO
    // =====================================================

    function mostrarEstado(
        mensaje,
        tipo = "info"
    ) {

        if (!estado) {
            return;
        }

        estado.style.display = "block";

        estado.textContent = mensaje;

        estado.style.padding = "10px 12px";

        estado.style.borderRadius = "8px";

        estado.style.fontSize = "12px";

        estado.style.marginBottom = "15px";


        // =================================================
        // INFO
        // =================================================

        if (tipo === "info") {

            estado.style.backgroundColor =
                "rgba(0, 212, 216, 0.08)";

            estado.style.color =
                "#00d4d8";

            estado.style.border =
                "1px solid rgba(0, 212, 216, 0.20)";
        }


        // =================================================
        // SUCCESS
        // =================================================

        else if (tipo === "success") {

            estado.style.backgroundColor =
                "rgba(34, 211, 166, 0.08)";

            estado.style.color =
                "#22d3a6";

            estado.style.border =
                "1px solid rgba(34, 211, 166, 0.20)";
        }


        // =================================================
        // WARNING
        // =================================================

        else if (tipo === "warning") {

            estado.style.backgroundColor =
                "rgba(255, 200, 87, 0.08)";

            estado.style.color =
                "#ffc857";

            estado.style.border =
                "1px solid rgba(255, 200, 87, 0.20)";
        }


        // =================================================
        // ERROR
        // =================================================

        else if (tipo === "error") {

            estado.style.backgroundColor =
                "#fee2e2";

            estado.style.color =
                "#b91c1c";

            estado.style.border =
                "1px solid #fecaca";
        }
    }


    // =====================================================
    // OCULTAR ESTADO
    // =====================================================

    function ocultarEstado() {

        if (!estado) {
            return;
        }

        estado.style.display = "none";

        estado.textContent = "";
    }


    // =====================================================
    // OBTENER UBICACIÓN
    // =====================================================

    function obtenerUbicacion() {

        return new Promise(function (
            resolve,
            reject
        ) {

            // -------------------------------------------------
            // VERIFICAR SOPORTE
            // -------------------------------------------------

            if (!navigator.geolocation) {

                reject(
                    new Error(
                        "Tu navegador no permite obtener la ubicación."
                    )
                );

                return;
            }


            // -------------------------------------------------
            // SOLICITAR UBICACIÓN
            // -------------------------------------------------

            navigator.geolocation.getCurrentPosition(

                function (position) {

                    const lat =
                        position.coords.latitude;

                    const lon =
                        position.coords.longitude;

                    const precision =
                        position.coords.accuracy;


                    // -------------------------------------------------
                    // VALIDAR COORDENADAS
                    // -------------------------------------------------

                    if (
                        typeof lat !== "number" ||
                        typeof lon !== "number"
                    ) {

                        reject(
                            new Error(
                                "El navegador no devolvió coordenadas válidas."
                            )
                        );

                        return;
                    }


                    // -------------------------------------------------
                    // GUARDAR COORDENADAS
                    // -------------------------------------------------

                    if (latitud) {

                        latitud.value =
                            lat.toFixed(7);
                    }


                    if (longitud) {

                        longitud.value =
                            lon.toFixed(7);
                    }


                    console.log(
                        "================================="
                    );

                    console.log(
                        "UBICACIÓN OBTENIDA"
                    );

                    console.log(
                        "Latitud:",
                        lat
                    );

                    console.log(
                        "Longitud:",
                        lon
                    );

                    console.log(
                        "Precisión:",
                        precision,
                        "metros"
                    );

                    console.log(
                        "================================="
                    );


                    resolve({

                        lat: lat,

                        lon: lon,

                        precision: precision

                    });

                },


                function (error) {

                    console.error(
                        "Error de geolocalización:",
                        error
                    );


                    let mensaje =
                        "No fue posible obtener tu ubicación.";


                    // -------------------------------------------------
                    // PERMISO DENEGADO
                    // -------------------------------------------------

                    if (
                        error.code ===
                        error.PERMISSION_DENIED
                    ) {

                        mensaje =
                            "Debes permitir el acceso a tu ubicación para registrar la entrada.";

                    }


                    // -------------------------------------------------
                    // UBICACIÓN NO DISPONIBLE
                    // -------------------------------------------------

                    else if (
                        error.code ===
                        error.POSITION_UNAVAILABLE
                    ) {

                        mensaje =
                            "La ubicación no está disponible. Verifica el GPS o la configuración de ubicación.";

                    }


                    // -------------------------------------------------
                    // TIMEOUT
                    // -------------------------------------------------

                    else if (
                        error.code ===
                        error.TIMEOUT
                    ) {

                        mensaje =
                            "La ubicación tardó demasiado en responder. Intenta nuevamente.";

                    }


                    reject(
                        new Error(mensaje)
                    );
                },


                {
                    enableHighAccuracy: true,

                    timeout: 20000,

                    maximumAge: 0

                }
            );

        });
    }


    // =====================================================
    // OBTENER DIRECCIÓN MEDIANTE NOMINATIM
    // =====================================================

    async function obtenerDireccion(
        lat,
        lon
    ) {

        const idioma =
            navigator.language || "es";


        const url =
            "https://nominatim.openstreetmap.org/reverse" +
            "?format=jsonv2" +
            "&lat=" +
            encodeURIComponent(lat) +
            "&lon=" +
            encodeURIComponent(lon) +
            "&zoom=18" +
            "&addressdetails=1" +
            "&accept-language=" +
            encodeURIComponent(idioma);


        console.log(
            "Consultando dirección..."
        );


        const respuesta =
            await fetch(
                url,
                {
                    method: "GET",

                    headers: {
                        "Accept":
                            "application/json"
                    }
                }
            );


        if (!respuesta.ok) {

            throw new Error(
                "El servicio de direcciones no respondió correctamente."
            );
        }


        const datos =
            await respuesta.json();


        return datos;
    }


    // =====================================================
// CREAR DIRECCIÓN CORTA
// =====================================================

function crearDireccionCorta(datos) {

    // =====================================================
    // VALIDAR RESPUESTA
    // =====================================================

    if (!datos) {
        return "";
    }


    // =====================================================
    // SI NO EXISTE ADDRESS
    // =====================================================

    if (!datos.address) {

        return datos.display_name || "";

    }


    const address = datos.address;


    // =====================================================
    // ARRAY DE PARTES
    // =====================================================

    const partes = [];


    // =====================================================
    // FUNCIÓN PARA AGREGAR VALORES
    // =====================================================

    function agregarParte(valor) {

        if (!valor) {
            return;
        }

        valor = String(valor).trim();

        if (!valor) {
            return;
        }

        // Evitar duplicados
        if (!partes.includes(valor)) {
            partes.push(valor);
        }

    }


    // =====================================================
    // LUGAR / EDIFICIO / EMPRESA
    // =====================================================

    const lugar =
        address.amenity ||
        address.shop ||
        address.office ||
        address.building ||
        address.tourism ||
        address.leisure ||
        address.hotel;

    agregarParte(lugar);


    // =====================================================
    // CALLE Y NÚMERO
    // =====================================================

    let calle = "";


    if (address.road) {

        calle = address.road.trim();

    }


    if (address.house_number) {

        if (calle) {

            calle += " " + address.house_number;

        } else {

            calle =
                address.house_number;

        }

    }


    agregarParte(calle);


    // =====================================================
    // BARRIO
    // =====================================================

    const barrio =
        address.neighbourhood ||
        address.suburb ||
        address.quarter ||
        address.residential;

    agregarParte(barrio);


    // =====================================================
    // CIUDAD
    // =====================================================

    const ciudad =
        address.city ||
        address.town ||
        address.village ||
        address.municipality ||
        address.city_district;

    agregarParte(ciudad);


    // =====================================================
    // DEPARTAMENTO / REGIÓN
    // =====================================================

    const region =
        address.state ||
        address.region;

    agregarParte(region);


    // =====================================================
    // PAÍS
    // =====================================================

    agregarParte(
        address.country
    );


    // =====================================================
    // RESULTADO
    // =====================================================

    if (partes.length > 0) {

        return partes.join(", ");

    }


    // =====================================================
    // RESPALDO
    // =====================================================

    return datos.display_name || "";

}


    // =====================================================
    // PREPARAR BOTÓN
    // =====================================================

    function botonCargando(
        mensaje
    ) {

        if (boton) {

            boton.disabled = true;
        }


        if (textoBoton) {

            textoBoton.textContent =
                mensaje;
        }


        if (iconoBoton) {

            iconoBoton.className =
                "bi bi-arrow-repeat";
        }
    }


    // =====================================================
    // RESTAURAR BOTÓN
    // =====================================================

    function restaurarBoton() {

        if (boton) {

            boton.disabled = false;
        }


        if (textoBoton) {

            textoBoton.textContent =
                "Iniciar sesión";
        }


        if (iconoBoton) {

            iconoBoton.className =
                "bi bi-arrow-right";
        }
    }


    // =====================================================
    // ENVÍO DEL FORMULARIO
    // =====================================================

    if (formulario) {

        formulario.addEventListener(
            "submit",
            async function (event) {

                // ---------------------------------------------
                // EVITAR ENVÍO NORMAL
                // ---------------------------------------------

                event.preventDefault();


                // ---------------------------------------------
                // EVITAR DOBLE ENVÍO
                // ---------------------------------------------

                if (
                    boton &&
                    boton.disabled
                ) {

                    return;
                }


                ocultarEstado();


                botonCargando(
                    "Obteniendo ubicación..."
                );


                try {

                    // =========================================
                    // 1. OBTENER UBICACIÓN
                    // =========================================

                    const ubicacion =
                        await obtenerUbicacion();


                    console.log(
                        "Coordenadas listas:",
                        ubicacion
                    );


                    mostrarEstado(
                        "Ubicación obtenida. Buscando dirección...",
                        "info"
                    );


                    // =========================================
                    // 2. OBTENER DIRECCIÓN
                    // =========================================

                    try {

                        const datos =
                            await obtenerDireccion(
                                ubicacion.lat,
                                ubicacion.lon
                            );


                        const direccionCorta =
                            crearDireccionCorta(
                                datos
                            );


                        // -----------------------------------------
                        // GUARDAR DIRECCIÓN
                        // -----------------------------------------

                        if (direccion) {

                            direccion.value =
                                datos.display_name ||
                                direccionCorta ||
                                "Dirección no disponible";
                        }


                        console.log(
                            "Dirección completa:",
                            datos.display_name
                        );


                        console.log(
                            "Dirección corta:",
                            direccionCorta
                        );


                        mostrarEstado(
                            "Ubicación registrada correctamente.",
                            "success"
                        );


                    } catch (errorDireccion) {

                        // -----------------------------------------
                        // LA DIRECCIÓN FALLÓ
                        // PERO LAS COORDENADAS SÍ EXISTEN
                        // -----------------------------------------

                        console.warn(
                            "No se pudo obtener la dirección:",
                            errorDireccion
                        );


                        if (direccion) {

                            direccion.value =
                                "Dirección no disponible";
                        }


                        mostrarEstado(
                            "Ubicación obtenida. La dirección no pudo determinarse.",
                            "warning"
                        );
                    }


                    // =========================================
                    // 3. ENVIAR FORMULARIO
                    // =========================================

                    botonCargando(
                        "Iniciando sesión..."
                    );


                    console.log(
                        "================================="
                    );

                    console.log(
                        "DATOS QUE SE ENVIARÁN AL SERVIDOR"
                    );

                    console.log(
                        "Zona horaria:",
                        zonaHoraria?.value
                    );

                    console.log(
                        "Latitud:",
                        latitud?.value
                    );

                    console.log(
                        "Longitud:",
                        longitud?.value
                    );

                    console.log(
                        "Dirección:",
                        direccion?.value
                    );

                    console.log(
                        "================================="
                    );


                    // ---------------------------------------------
                    // SUBMIT NATIVO
                    // ---------------------------------------------

                    HTMLFormElement.prototype.submit.call(
                        formulario
                    );

                } catch (error) {

                    // =========================================
                    // ERROR GENERAL
                    // =========================================

                    console.error(
                        "Error durante el inicio de sesión:",
                        error
                    );


                    mostrarEstado(
                        error.message ||
                        "No fue posible obtener tu ubicación.",
                        "error"
                    );


                    restaurarBoton();
                }

            }
        );
    }


    // =====================================================
    // OCULTAR ALERTAS FLASK AUTOMÁTICAMENTE
    // =====================================================

    const alerts =
        document.querySelectorAll(
            ".login-alert"
        );


    alerts.forEach(
        function (alert) {

            setTimeout(
                function () {

                    alert.classList.add(
                        "login-alert-hide"
                    );


                    setTimeout(
                        function () {

                            alert.remove();

                        },
                        350
                    );

                },
                4000
            );

        }
    );

});
