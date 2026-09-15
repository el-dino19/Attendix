// =========================================================
// DASHBOARD EMPLEADO
// =========================================================

document.addEventListener("DOMContentLoaded", function () {

    // =====================================================
    // RELOJ DIGITAL
    // =====================================================

    function actualizarReloj() {

        const reloj = document.getElementById("reloj");
        const fecha = document.getElementById("fecha-actual");

        if (!reloj) {
            return;
        }

        const ahora = new Date();

        // Colombia
        const opcionesHora = {
            timeZone: "America/Bogota",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hour12: true
        };

        const opcionesFecha = {
            timeZone: "America/Bogota",
            weekday: "long",
            year: "numeric",
            month: "long",
            day: "numeric"
        };

        const horaColombia = new Intl.DateTimeFormat(
            "es-CO",
            opcionesHora
        ).format(ahora);

        const fechaColombia = new Intl.DateTimeFormat(
            "es-CO",
            opcionesFecha
        ).format(ahora);

        reloj.textContent = horaColombia;

        if (fecha) {
            fecha.textContent = fechaColombia;
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

    const mensajes = document.querySelectorAll(
        ".custom-toast"
    );

    mensajes.forEach(function (mensaje) {

        // Esperar 4 segundos
        setTimeout(function () {

            mensaje.classList.add(
                "toast-hide"
            );

            // Eliminar después de la animación
            setTimeout(function () {

                mensaje.remove();

            }, 400);

        }, 4000);

    });


    // =====================================================
    // CONTADOR DE DESCANSO
    // =====================================================

    const contador =
        document.getElementById("contador");

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
    // BOTÓN FINALIZAR DESCANSO
    // =====================================================

    const formularioDescanso =
        document.getElementById(
            "form-finalizar-descanso"
        );

    if (formularioDescanso) {

        formularioDescanso.addEventListener(
            "submit",
            function () {

                const boton =
                    formularioDescanso.querySelector(
                        "button"
                    );

                if (boton) {

                    boton.disabled = true;

                    boton.innerHTML =
                        '<i class="bi bi-hourglass-split"></i> FINALIZANDO...';

                }

            }
        );

    }

});


// =========================================================
// CONTADOR DE DESCANSO
// =========================================================

function iniciarContadorDescanso(contador) {

    const mensaje =
        document.getElementById(
            "mensaje-contador"
        );

    const tipo =
        (contador.dataset.tipo || "").trim();

    const horaInicio =
        (contador.dataset.inicio || "").trim();


    // -----------------------------------------------------
    // DURACIONES
    // -----------------------------------------------------

    const duraciones = {

        break_manana: 15 * 60,

        lunch: 60 * 60,

        break_tarde: 15 * 60

    };


    const duracionTotal =
        duraciones[tipo];


    if (!duracionTotal) {

        contador.textContent = "00:00";

        if (mensaje) {

            mensaje.textContent =
                "Tipo de descanso no válido.";

        }

        return;
    }


    // -----------------------------------------------------
    // CONVERTIR HORA
    // -----------------------------------------------------

    function convertirHoraASegundos(hora) {

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

        contador.textContent = "00:00";

        if (mensaje) {

            mensaje.textContent =
                "No se pudo calcular el tiempo.";

        }

        return;
    }


    // -----------------------------------------------------
    // HORA ACTUAL COLOMBIA
    // -----------------------------------------------------

    function obtenerHoraActualSegundos() {

        const ahora =
            new Date();


        const partes =
            new Intl.DateTimeFormat(
                "en-US",
                {
                    timeZone: "America/Bogota",
                    hour: "2-digit",
                    minute: "2-digit",
                    second: "2-digit",
                    hour12: false
                }
            ).formatToParts(ahora);


        let horas = 0;
        let minutos = 0;
        let segundos = 0;


        partes.forEach(function (parte) {

            if (parte.type === "hour") {
                horas = Number(parte.value);
            }

            if (parte.type === "minute") {
                minutos = Number(parte.value);
            }

            if (parte.type === "second") {
                segundos = Number(parte.value);
            }

        });


        return (
            horas * 3600 +
            minutos * 60 +
            segundos
        );
    }


    // -----------------------------------------------------
    // TIEMPO TRANSCURRIDO
    // -----------------------------------------------------

    function obtenerTiempoTranscurrido() {

        const actual =
            obtenerHoraActualSegundos();


        let diferencia =
            actual - inicioSegundos;


        if (diferencia < 0) {

            diferencia +=
                24 * 60 * 60;

        }


        return diferencia;
    }


    // -----------------------------------------------------
    // FORMATEAR
    // -----------------------------------------------------

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
            String(minutos).padStart(2, "0") +
            ":" +
            String(segundosRestantes).padStart(2, "0")
        );
    }


    // -----------------------------------------------------
    // ACTUALIZAR
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
// CONTADOR HORAS EXTRAS
// =========================================================

function iniciarContadorHorasExtras(
    contador
) {

    const inicio =
        contador.dataset.inicio;


    if (!inicio) {

        return;

    }


    const fechaInicio =
        new Date(inicio);


    if (isNaN(fechaInicio.getTime())) {

        contador.textContent =
            "00:00:00";

        return;

    }


    function actualizar() {

        const ahora =
            new Date();


        let diferencia =
            Math.floor(
                (ahora - fechaInicio) / 1000
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
                (diferencia % 3600) / 60
            );


        const segundos =
            diferencia % 60;


        contador.textContent =
            String(horas).padStart(2, "0") +
            ":" +
            String(minutos).padStart(2, "0") +
            ":" +
            String(segundos).padStart(2, "0");
    }


    actualizar();


    setInterval(
        actualizar,
        1000
    );
}


// =========================================================
// INICIAR HORAS EXTRAS
// =========================================================

async function iniciarHorasExtras() {

    if (!navigator.geolocation) {

        alert(
            "Tu navegador no permite obtener la ubicación."
        );

        return;
    }


    const boton =
        document.querySelector(
            "[onclick='iniciarHorasExtras()']"
        );


    if (boton) {

        boton.disabled = true;

        boton.innerHTML =
            '<i class="bi bi-hourglass-split"></i> OBTENIENDO UBICACIÓN...';

    }


    navigator.geolocation.getCurrentPosition(

        async function (position) {

            const latitud =
                position.coords.latitude;

            const longitud =
                position.coords.longitude;


            try {

                const response =
                    await fetch(
                        "/Attendix/horas-extras/iniciar",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                latitud: latitud,
                                longitud: longitud,
                                ubicacion:
                                    `${latitud}, ${longitud}`
                            })
                        }
                    );


                const data =
                    await response.json();


                if (!response.ok || !data.exito) {

                    throw new Error(
                        data.mensaje ||
                        "No se pudieron iniciar las horas extras."
                    );

                }


                window.location.reload();


            } catch (error) {

                alert(
                    error.message
                );


                if (boton) {

                    boton.disabled = false;

                    boton.innerHTML =
                        '<i class="bi bi-clock-fill"></i> INICIAR HORAS EXTRAS';

                }

            }

        },

        function (error) {

            let mensaje =
                "No se pudo obtener tu ubicación.";


            if (
                error.code ===
                error.PERMISSION_DENIED
            ) {

                mensaje =
                    "Debes permitir el acceso a tu ubicación para iniciar horas extras.";

            }


            alert(
                mensaje
            );


            if (boton) {

                boton.disabled = false;

                boton.innerHTML =
                    '<i class="bi bi-clock-fill"></i> INICIAR HORAS EXTRAS';

            }

        },

        {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        }

    );
}


// =========================================================
// FINALIZAR HORAS EXTRAS
// =========================================================

async function finalizarHorasExtras() {

    if (!navigator.geolocation) {

        alert(
            "Tu navegador no permite obtener la ubicación."
        );

        return;
    }


    const boton =
        document.querySelector(
            "[onclick='finalizarHorasExtras()']"
        );


    if (boton) {

        boton.disabled = true;

        boton.innerHTML =
            '<i class="bi bi-hourglass-split"></i> FINALIZANDO...';

    }


    navigator.geolocation.getCurrentPosition(

        async function (position) {

            const latitud =
                position.coords.latitude;

            const longitud =
                position.coords.longitude;


            try {

                const response =
                    await fetch(
                        "/Attendix/horas-extras/finalizar",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                latitud: latitud,
                                longitud: longitud,
                                ubicacion:
                                    `${latitud}, ${longitud}`
                            })
                        }
                    );


                const data =
                    await response.json();


                if (!response.ok || !data.exito) {

                    throw new Error(
                        data.mensaje ||
                        "No se pudieron finalizar las horas extras."
                    );

                }


                window.location.reload();


            } catch (error) {

                alert(
                    error.message
                );


                if (boton) {

                    boton.disabled = false;

                    boton.innerHTML =
                        '<i class="bi bi-stop-circle-fill"></i> FINALIZAR HORAS EXTRAS';

                }

            }

        },

        function () {

            alert(
                "Debes permitir el acceso a tu ubicación para finalizar las horas extras."
            );


            if (boton) {

                boton.disabled = false;

                boton.innerHTML =
                    '<i class="bi bi-stop-circle-fill"></i> FINALIZAR HORAS EXTRAS';

            }

        },

        {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        }

    );
}
