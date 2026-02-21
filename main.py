import subprocess
from fastapi import FastAPI

app = FastAPI()

@app.get("/crawl")
def crawl(url: str):
    try:
        # Ejecutamos el comando de consola directamente desde Python
        # 'scrapy runspider' nos permite correr un archivo .py sin crear un proyecto completo
        # -a url=... pasa la URL como argumento al spider
        # -o output.json guarda el resultado en un archivo
        subprocess.run(
            ["scrapy", "runspider", "scraper.py", "-a", f"url={url}", "-o", "output.json"],
            check=True
        )
        
        return {"status": "scraping_finished", "note": "Revisa el archivo output.json o los logs"}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
