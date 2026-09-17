// =====================================================
// COMPROBAR ESTADO DE LA CUENTA CADA 10 SEGUNDOS
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
