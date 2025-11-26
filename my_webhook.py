from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configuración para producción
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"


# Ruta para verificar que la API está funcionando
@app.route("/", methods=["GET"])
def home():
    return jsonify(
        {"status": "running", "message": "API de Webhook funcionando correctamente"}
    )


@app.route("/webhook/scrapper_status", methods=["GET"])
def webhook_scrapper_statñus():
    try:
        # Usa una ruta absoluta para el archivo
        file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "scrapper_status.txt"
        )

        with open(file_path, "r", encoding="utf-8") as f:
            status = f.read().strip().lower()
        if status == "success":
            return jsonify(
                {"status": "success", "message": "Scrapper ejecutado correctamente."}
            )
        elif status == "error":
            return jsonify(
                {"status": "error", "message": "Hubo un error en el scrapper."}
            )
        else:
            return jsonify(
                {"status": "unknown", "message": f"Estado desconocido: {status}"}
            )
    except FileNotFoundError:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "No se encontró el archivo de estado del scrapper.",
                }
            ),
            404,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"Error al consultar el estado: {str(e)}",
                }
            ),
            500,
        )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=DEBUG)
