 let cuentaDesactivada = false;

    async function verificarEstadoCuenta() {

        if (cuentaDesactivada) {
            return;
        }

        try {

            const response = await fetch(
                "{{ url_for('auth.verificar_estado') }}",
                {
                    method: "GET",
                    credentials: "same-origin",
                    cache: "no-store"
                }
            );

            if (!response.ok) {
                return;
            }

            const data = await response.json();

            if (data.activo === false) {

                cuentaDesactivada = true;

                const modalElement =
                    document.getElementById(
                        "modalCuentaDesactivada"
                    );

                if (!modalElement) {
                    console.error(
                        "No se encontró la modal"
                    );
                    return;
                }

                const modal =
                    new bootstrap.Modal(
                        modalElement,
                        {
                            backdrop: "static",
                            keyboard: false
                        }
                    );

                modal.show();


                // =====================================
                // CUENTA REGRESIVA DE 10 SEGUNDOS
                // =====================================

                let segundos = 10;

                const contador =
                    document.getElementById(
                        "contadorDesactivacion"
                    );

                if (contador) {
                    contador.textContent = segundos;
                }

                const intervalo =
                    setInterval(function () {

                        segundos--;

                        if (contador) {
                            contador.textContent = segundos;
                        }

                        if (segundos <= 0) {

                            clearInterval(intervalo);

                            window.location.href =
                                "{{ url_for('auth.logout') }}";
                        }

                    }, 1000);
            }

        } catch (error) {

            console.error(
                "Error verificando estado:",
                error
            );

        }
    }


    // =====================================
    // VERIFICAR AL CARGAR
    // =====================================

    verificarEstadoCuenta();


    // =====================================
    // VERIFICAR CADA 5 SEGUNDOS
    // =====================================

    setInterval(
        verificarEstadoCuenta,
        5000
    );


    // =====================================
    // BOTÓN "ENTENDIDO"
    // =====================================

    const boton =
        document.getElementById(
            "btnCuentaDesactivada"
        );

    if (boton) {

        boton.addEventListener(
            "click",
            function () {

                window.location.href =
                    "{{ url_for('auth.logout') }}";

            }
        );
    }