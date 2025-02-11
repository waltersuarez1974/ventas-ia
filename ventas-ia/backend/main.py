from fastapi import FastAPI, HTTPException
import mysql.connector
import openai
import os

app = FastAPI()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "tu-servidor.mysql.database.azure.com"),
    "user": os.getenv("DB_USER", "tu_usuario"),
    "password": os.getenv("DB_PASSWORD", "tu_contraseña"),
    "database": os.getenv("DB_NAME", "ventas_db")
}

openai.api_type = "azure"
openai.api_key = os.getenv("OPENAI_API_KEY", "TU_API_KEY")
openai.api_base = "https://tu-endpoint-openai.openai.azure.com/"
openai.api_version = "2023-12-01-preview"

def obtener_datos_cliente(cliente_nombre):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, limite_credito FROM clientes WHERE nombre = %s", (cliente_nombre,))
        cliente = cursor.fetchone()
        if not cliente:
            return None

        cursor.execute("SELECT SUM(monto) AS total_ventas FROM ventas WHERE cliente_id = %s", (cliente["id"],))
        total_ventas = cursor.fetchone()["total_ventas"] or 0

        cursor.execute("SELECT SUM(monto) AS total_cobranzas FROM cobranzas WHERE cliente_id = %s", (cliente["id"],))
        total_cobranzas = cursor.fetchone()["total_cobranzas"] or 0

        return {
            "nombre": cliente_nombre,
            "limite_credito": cliente["limite_credito"],
            "total_ventas": total_ventas,
            "total_cobranzas": total_cobranzas
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.get("/evaluar_cliente/{cliente_nombre}")
async def evaluar_cliente(cliente_nombre: str):
    datos = obtener_datos_cliente(cliente_nombre)
    if not datos:
        return {"mensaje": "Cliente no encontrado"}

    prompt = f"""
    Un cliente llamado {datos['nombre']} tiene un límite de crédito de {datos['limite_credito']} USD.
    Sus ventas acumuladas suman {datos['total_ventas']} USD.
    Sus cobranzas acumuladas suman {datos['total_cobranzas']} USD.
    Basado en esta información, ¿es recomendable venderle más crédito?
    """

    response = openai.ChatCompletion.create(
        engine="gpt-4",
        messages=[{"role": "system", "content": "Eres un analista financiero experto en crédito."},
                  {"role": "user", "content": prompt}]
    )

    decision = response["choices"][0]["message"]["content"]
    return {"cliente": datos["nombre"], "evaluacion": decision}
