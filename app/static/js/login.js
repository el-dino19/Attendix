document.addEventListener("DOMContentLoaded", function () {

    // =====================================================
    // ELEMENTOS
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
        zonaHoraria.value = Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC";
    }


    // =====================================================
    // MOSTRAR / OCULTAR CONTRASEÑA
    // =====================================================
    if (passwordInput && togglePassword && passwordIcon) {
        togglePassword.addEventListener("click", function () {
            if (passwordInput.type === "password") {
                passwordInput.type = "text";
                passwordIcon.classList.remove("bi-eye");
                passwordIcon.classList.add("bi-eye-slash");
                togglePassword.setAttribute("aria-label", "Ocultar contraseña");
            } else {
                passwordInput.type = "password";
                passwordIcon.classList.remove("bi-eye-slash");
                passwordIcon.classList.add("bi-eye");
                togglePassword.setAttribute("aria-label", "Mostrar contraseña");
            }
        });
    }


    // =====================================================
    // MOSTRAR MENSAJE DE UBICACIÓN
    // =====================================================
    function mostrarError(mensaje) {
        if (!estado) return;
        estado.style.display = "block";
        estado.style.backgroundColor = "#fee2e2";
        estado.style.color = "#b91c1c";
        estado.style.border = "1px solid #fecaca";
        estado.textContent = mensaje;
    }


    // =====================================================
    // OCULTAR MENSAJE
    // =====================================================
    function ocultarMensaje() {
        if (!estado) return;
        estado.style.display = "none";
        estado.textContent = "";
    }


    // =====================================================
    // OBTENER UBICACIÓN
    // =====================================================
    function obtenerUbicacion() {
        return new Promise(function (resolve, reject) {
            if (!navigator.geolocation) {
                reject(new Error("Tu navegador no permite obtener la ubicación."));
                return;
            }

            navigator.geolocation.getCurrentPosition(
                function (position) {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;

                    if (latitud) latitud.value = lat;
                    if (longitud) longitud.value = lon;

                    resolve({ lat: lat, lon: lon });
                },
                function (error) {
                    let mensaje = "No fue posible obtener tu ubicación.";

                    if (error.code === error.PERMISSION_DENIED) {
                        mensaje = "Debes permitir el acceso a tu ubicación para iniciar sesión.";
                    } else if (error.code === error.POSITION_UNAVAILABLE) {
                        mensaje = "La ubicación no está disponible. Verifica la configuración de ubicación de tu dispositivo.";
                    } else if (error.code === error.TIMEOUT) {
                        mensaje = "No se pudo obtener tu ubicación a tiempo. Intenta nuevamente.";
                    }

                    reject(new Error(mensaje));
                },
                {
                    enableHighAccuracy: true,
                    timeout: 15000,
                    maximumAge: 0
                }
            );
        });
    }


    // =====================================================
    // OBTENER DIRECCIÓN COMPLETA
    // =====================================================
    async function obtenerDireccion(lat, lon) {
        const url = "https://nominatim.openstreetmap.org/reverse" +
            "?format=jsonv2" +
            "&lat=" + encodeURIComponent(lat) +
            "&lon=" + encodeURIComponent(lon) +
            "&zoom=18" +
            "&addressdetails=1" +
            "&accept-language=" + encodeURIComponent(navigator.language || "es");

        const respuesta = await fetch(url, {
            headers: {
                "Accept": "application/json"
            }
        });

        if (!respuesta.ok) {
            throw new Error("No se pudo consultar la dirección.");
        }

        return await respuesta.json();
    }


    // =====================================================
    // CREAR DIRECCIÓN CORTA
    // =====================================================
    function crearDireccionCorta(datos) {
        if (!datos || !datos.address) {
            return datos?.display_name || "";
        }

        const address = datos.address;
        const partes = [];

        // 1. LUGAR / EDIFICIO / COMERCIO
        const lugar = address.amenity || address.shop || address.tourism || address.building || address.office || address.leisure || address.hotel;
        if (lugar) partes.push(lugar);

        // 2. NÚMERO Y CALLE
        let calle = "";
        if (address.house_number) calle += address.house_number;
        if (address.road) {
            if (calle) calle += ", ";
            calle += address.road;
        }
        if (calle) partes.push(calle);

        // 3. BARRIO / DISTRITO
        const barrio = address.neighbourhood || address.suburb || address.quarter || address.residential;
        if (barrio && !partes.includes(barrio)) partes.push(barrio);

        // 4. CIUDAD
        const ciudad = address.city || address.town || address.village || address.municipality;
        if (ciudad && !partes.includes(ciudad)) partes.push(ciudad);

        // 5. ESTADO / REGIÓN
        const estadoPais = address.state || address.region;
        if (estadoPais && !partes.includes(estadoPais)) partes.push(estadoPais);

        // 6. PAÍS
        if (address.country) partes.push(address.country);

        // LIMPIAR DUPLICADOS
        const resultado = partes.filter(function (valor, indice) {
            return valor && partes.indexOf(valor) === indice;
        });

        return resultado.join(", ");
    }


    // =====================================================
    // ENVÍO DEL FORMULARIO
    // =====================================================
    if (formulario) {
        formulario.addEventListener("submit", async function (event) {
            event.preventDefault();

            if (boton) boton.disabled = true;
            ocultarMensaje();

            try {
                // 1. OBTENER UBICACIÓN
                const ubicacion = await obtenerUbicacion();
                console.log("Latitud:", ubicacion.lat);
                console.log("Longitud:", ubicacion.lon);

                // 2. OBTENER DIRECCIÓN
                try {
                    const datos = await obtenerDireccion(ubicacion.lat, ubicacion.lon);

                    if (direccion) {
                        direccion.value = datos.display_name || "";
                    }

                    const direccionCorta = crearDireccionCorta(datos);
                    console.log("Dirección completa:", datos.display_name);
                    console.log("Dirección corta:", direccionCorta);

                } catch (error) {
                    console.warn("No se pudo obtener la dirección:", error);
                    if (direccion) {
                        direccion.value = "Dirección no disponible";
                    }
                }

                // 3. CAMBIAR BOTÓN
                if (textoBoton) textoBoton.textContent = "Iniciando sesión...";
                if (iconoBoton) iconoBoton.className = "bi bi-arrow-right";

                // 4. ENVIAR FORMULARIO
                formulario.submit();

            } catch (error) {
                console.error("Error obteniendo ubicación:", error);
                mostrarError(error.message);

                if (boton) boton.disabled = false;
                if (textoBoton) textoBoton.textContent = "Iniciar sesión";
                if (iconoBoton) iconoBoton.className = "bi bi-arrow-right";
            }
        });
    }


    // =====================================================
    // OCULTAR ALERTAS FLASK
    // =====================================================
    const alerts = document.querySelectorAll(".login-alert");

    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.classList.add("login-alert-hide");

            setTimeout(function () {
                alert.remove();
            }, 350);
        }, 4000);
    });

});