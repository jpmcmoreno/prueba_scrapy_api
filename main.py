from fastapi import FastAPI
from scrapy.crawler import CrawlerRunner
from crochet import setup, wait_for
from scraper import MiSpider # Importamos tu spider

# Inicializa crochet para manejar los hilos de Scrapy/Twisted
setup()

app = FastAPI()
runner = CrawlerRunner()

# Variable global para guardar resultados temporalmente
results = []

@app.get("/")
def home():
    return {"message": "API de Scrapy lista. Usa /crawl?url=URL_AQUÍ"}

@app.get("/crawl")
def crawl(url: str):
    # Limpiamos resultados anteriores
    results.clear()
    
    # Ejecutamos el spider de forma asíncrona
    run_spider_in_background(url)
    
    return {"status": "request_received", "url": url, "note": "Revisa la consola de Render para ver el progreso"}

@wait_for(timeout=20.0)
def run_spider_in_background(url):
    # Definimos dónde guardar el resultado al terminar
    deferred = runner.crawl(MiSpider, url=url)
    deferred.addCallback(collect_results)
    return deferred

def collect_results(item):
    results.append(item)
    print(f"Resultado obtenido: {item}")
    return item
