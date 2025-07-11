from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import requests
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const
import pytz

app = FastAPI()

OPENCAGE_API_KEY = "3424b3aea9e64ebfbc6b54cd143f6c81"

class MapaAstralRequest(BaseModel):
    nome: str
    data_nascimento: str  # Formato: YYYY-MM-DD
    hora_nascimento: str  # Formato: HH:MM
    cidade_nascimento: str

def get_coordinates(city):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city}&key={OPENCAGE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if not data['results']:
        raise HTTPException(status_code=400, detail="Localização não encontrada")
    geometry = data['results'][0]['geometry']
    return geometry['lat'], geometry['lng']

@app.post("/mapa-astral")
def gerar_mapa_astral(req: MapaAstralRequest):
    try:
        lat, lon = get_coordinates(req.cidade_nascimento)

        local_tz = pytz.timezone("America/Sao_Paulo")
        local_dt = datetime.strptime(f"{req.data_nascimento} {req.hora_nascimento}", "%Y-%m-%d %H:%M")
        localized_dt = local_tz.localize(local_dt)
        utc_dt = localized_dt.astimezone(pytz.utc)

        date = Datetime(utc_dt.strftime('%Y/%m/%d'), utc_dt.strftime('%H:%M'), '+00:00')
        pos = GeoPos(lat, lon)

        chart = Chart(date, pos, hsys=const.HOUSES_EQUAL)
        sol = chart.get(const.SUN)
        lua = chart.get(const.MOON)
        asc = chart.get(const.ASC)

        casas = {f"casa_{i}": chart.get(f"House{i}").sign for i in range(1, 13)}

        return {
            "nome": req.nome,
            "sol": f"{sol.sign} {sol.lon:.2f}",
            "lua": f"{lua.sign} {lua.lon:.2f}",
            "ascendente": asc.sign,
            **casas
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
