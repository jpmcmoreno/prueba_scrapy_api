from fastapi import FastAPI
import subprocess
import json
import os
import uuid

app = FastAPI()

@app.get("/crawl")
def crawl(url: str):
    # Generamos un nombre de archivo único para que si dos personas
    # usan la API al mismo tiempo, no se mezclen los datos.
    unique_id = str(uuid.uuid4())[:8]
    output_file = f"result_{unique_id}.json"

    try:
        # 1. Ejecutamos Scrapy y ESPERAMOS a que termine (check=True)
        # El programa se detendrá aquí hasta que el scraping acabe.
        subprocess.run(
            ["scrapy", "runspider", "scraper.py", "-a", f"url={url}", "-o", output_file],
            check=True,
            capture_output=True # Esto ayuda a capturar errores de consola si fallara
        )

        # 2. Verificamos si Scrapy creó el archivo y tiene datos
        if os.path.exists(output_file):
            with open(output_file, "r") as f:
                data = json.load(f)
            
            # 3. Borramos el archivo temporal para no llenar el disco de Render
            os.remove(output_file)
            
            # 4. ¡LA MAGIA! Devolvemos los datos directamente como respuesta JSON
            return {
                "status": "success",
                "target_url": url,
                "scraped_data": data
            }
        else:
            return {"status": "error", "message": "El scraper terminó pero no encontró datos."}

    except subprocess.CalledProcessError as e:
        return {
            "status": "error", 
            "message": "Scrapy falló", 
            "details": e.stderr.decode() if e.stderr else "Error desconocido"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
