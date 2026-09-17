setInterval(async function () {
    try {
        const response = await fetch("{{ url_for('auth.check_session') }}", {
            method: "GET",
            credentials: "same-origin",
            cache: "no-store"
        });

        const data = await response.json();

        // Usuario sigue activo (activo = 1)
        if (data.activo === true) {
            return;
        }

        // Usuario fue desactivado (activo = 0)
        if (
            data.activo === false &&
            data.sesion === true &&
            data.motivo === "cuenta_desactivada"
        ) {

            // No mostrar la modal más de una vez
            if (document.getElementById("cuenta-desactivada-modal")) {
                return;
            }

            const modal = document.createElement("div");

            modal.id = "cuenta-desactivada-modal";

            modal.innerHTML = `
                <div style="
                    position: fixed;
                    inset: 0;
                    background: rgba(15, 23, 42, 0.65);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 99999;
                ">

                    <div style="
                        background: white;
                        width: min(420px, 90%);
                        border-radius: 20px;
                        padding: 32px;
                        text-align: center;
                        box-shadow: 0 20px 50px rgba(0,0,0,0.2);
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
                            margin-bottom: 10px;
                            color: #1e293b;
                        ">
                            Cuenta desactivada
                        </h3>

                        <p style="
                            color: #64748b;
                            margin-bottom: 25px;
                        ">
                            Tu cuenta ha sido desactivada por un administrador.
                            Ya no puedes continuar utilizando la aplicación.
                        </p>

                        <button
                            onclick="window.location.href='{{ url_for('auth.login') }}'"
                            style="
                                border: none;
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
        }

    } catch (error) {
        console.error(
            "Error comprobando el estado de la cuenta:",
            error
        );
    }

}, 5000);
