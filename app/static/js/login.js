document.addEventListener("DOMContentLoaded", function () {

    // =====================================================
    // ELEMENTOS
    // =====================================================
    const formulario = document.getElementById("loginForm");
    const boton = document.getElementById("loginButton");
    const textoBoton = document.getElementById("loginButtonText");
    const iconoBoton = document.getElementById("loginButtonIcon");
    const estado = document.getElementById("estado-ubicacion");
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
    // MOSTRAR ERROR
    // =====================================================
    function mostrarError(mensaje) {
        if (!estado) return;
        estado.style.display = "block";
        estado.style.background = "#fee2e2";
        estado.style.color = "#b91c1c";
        estado.textContent = mensaje;
    }


    // =====================================================
    // MOSTRAR ÉXITO
    // =====================================================
    function mostrarExito(mensaje) {
        if (!estado) return;
        estado.style.display = "block";
        estado.style.background = "#dcfce7";
        estado.style.color = "#166534";
        estado.textContent = mensaje;
    }


    // =====================================================
    // OBTENER UBICACIÓN
    // =====================================================
    function obtenerUbicacion() {
        return new Promise(function (resolve, reject) {
            if (!navigator.geolocation) {
                reject(new Error("La ubicación no está disponible en este navegador."));
                return;
            }

            /* El navegador mostrará su propio permiso de ubicación. */
            navigator.geolocation.getCurrentPosition(
                function (position) {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;

                    latitud.value = lat;
                    longitud.value = lon;

                    resolve({ lat: lat, lon: lon });
                },
                function (error) {
                    let mensaje;

                    if (error.code === error.PERMISSION_DENIED) {
                        mensaje = "Para registrar tu jornada, debes permitir el acceso a tu ubicación desde el navegador.";
                    } else if (error.code === error.POSITION_UNAVAILABLE) {
                        mensaje = "No pudimos determinar tu ubicación. Verifica que la ubicación esté activada en tu dispositivo.";
                    } else if (error.code === error.TIMEOUT) {
                        mensaje = "La ubicación está tardando demasiado en responder. Intenta nuevamente.";
                    } else {
                        mensaje = "No pudimos obtener tu ubicación. Intenta nuevamente.";
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
    // OBTENER DIRECCIÓN
    // =====================================================
    async function obtenerDireccion(lat, lon) {
        const url = "https://nominatim.openstreetmap.org/reverse" +
            "?format=jsonv2" +
            "&lat=" + encodeURIComponent(lat) +
            "&lon=" + encodeURIComponent(lon) +
            "&zoom=18" +
            "&addressdetails=1";

        const respuesta = await fetch(url, {
            headers: {
                "Accept": "application/json"
            }
        });

        if (!respuesta.ok) {
            throw new Error("No se pudo obtener la dirección.");
        }

        return await respuesta.json();
    }


    // =====================================================
    // CREAR DIRECCIÓN CORTA
    // =====================================================
    function crearDireccionCorta(datos) {
        if (!datos) return "";
        if (!datos.address) return datos.display_name || "";

        const address = datos.address;
        const partes = [];

        // LUGAR
        const lugar = address.amenity || address.shop || address.tourism || address.hotel || address.building || address.office;
        if (lugar) partes.push(lugar);

        // CALLE
        if (address.road) {
            let calle = address.road;
            if (address.house_number) {
                calle += ", " + address.house_number;
            }
            partes.push(calle);
        }

        // BARRIO / ZONA
        const barrio = address.neighbourhood || address.suburb || address.quarter || address.district;
        if (barrio) partes.push(barrio);

        // CIUDAD
        const ciudad = address.city || address.town || address.village || address.municipality;
        if (ciudad && !partes.includes(ciudad)) {
            partes.push(ciudad);
        }

        // ESTADO / PROVINCIA
        const estadoRegion = address.state || address.region || address.province;
        if (estadoRegion && !partes.includes(estadoRegion)) {
            partes.push(estadoRegion);
        }

        // PAÍS
        if (address.country) {
            partes.push(address.country);
        }

        // ELIMINAR DUPLICADOS
        const resultado = [...new Set(partes)];
        if (resultado.length > 0) {
            return resultado.join(", ");
        }

        return datos.display_name || "";
    }


    // =====================================================
    // LOGIN
    // =====================================================
    if (formulario) {
        formulario.addEventListener("submit", async function (event) {
            event.preventDefault();

            // Evitar doble clic
            boton.disabled = true;

            try {
                // OBTENER UBICACIÓN
                const ubicacion = await obtenerUbicacion();

                // OBTENER DIRECCIÓN
                try {
                    const datos = await obtenerDireccion(ubicacion.lat, ubicacion.lon);
                    const direccionCorta = crearDireccionCorta(datos);
                    direccion.value = direccionCorta || "Dirección no disponible";
                } catch (error) {
                    console.warn("No se pudo obtener la dirección:", error);
                    direccion.value = "Dirección no disponible";
                }

                // MENSAJE
                mostrarExito("Ubicación obtenida correctamente. Iniciando sesión...");

                // CAMBIAR BOTÓN
                textoBoton.textContent = "Iniciando sesión...";
                iconoBoton.className = "bi bi-arrow-right";

                // ENVIAR FORMULARIO
                formulario.submit();

            } catch (error) {
                console.error("Error obteniendo ubicación:", error);
                mostrarError(error.message);

                boton.disabled = false;
                textoBoton.textContent = "Iniciar sesión";
                iconoBoton.className = "bi bi-arrow-right";
            }
        });
    }


    // =====================================================
    // MOSTRAR / OCULTAR CONTRASEÑA
    // =====================================================
    const passwordInput = document.getElementById("password");
    const togglePassword = document.getElementById("togglePassword");
    const passwordIcon = document.getElementById("passwordIcon");

    if (passwordInput && togglePassword && passwordIcon) {
        togglePassword.addEventListener("click", function () {
            if (passwordInput.type === "password") {
                passwordInput.type = "text";
                passwordIcon.classList.remove("bi-eye");
                passwordIcon.classList.add("bi-eye-slash");
            } else {
                passwordInput.type = "password";
                passwordIcon.classList.remove("bi-eye-slash");
                passwordIcon.classList.add("bi-eye");
            }
        });
    }


    // =====================================================
    // OCULTAR MENSAJES FLASK
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