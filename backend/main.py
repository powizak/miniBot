from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, WebSocket
from backend import api
from backend.db import engine, influx_client
from backend.scheduler import start_scheduler

app = FastAPI(title="miniBot Backend")

# Registrace routeru pro správu botů
app.include_router(api.router)

# Websocket endpoint pro real-time data
import asyncio
from backend.db import influx_client, INFLUXDB_ORG
from influxdb_client.client.write_api import SYNCHRONOUS

@app.websocket("/ws/realtime")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        for _ in range(10):
            # Získání posledního ticku z InfluxDB
            try:
                query = f'''
                  from(bucket: "minibot")
                  |> range(start: -1m)
                  |> filter(fn: (r) => r._measurement == "trades")
                  |> last()
                '''
                tables = influx_client.query_api().query(query, org=INFLUXDB_ORG)
                price, volume, timestamp = None, None, None
                for table in tables:
                    for record in table.records:
                        if record.get_field() == "price":
                            price = record.get_value()
                            timestamp = record.get_time().timestamp()
                        if record.get_field() == "volume":
                            volume = record.get_value()
                data = {
                    "price": price,
                    "volume": volume,
                    "timestamp": timestamp
                }
            except Exception:
                data = {
                    "price": None,
                    "volume": None,
                    "timestamp": None
                }
            await websocket.send_json(data)
            await asyncio.sleep(1)
    except Exception:
        pass
    finally:
        await websocket.close()

# Inicializace plánovače úloh při startu aplikace
@app.on_event("startup")
async def startup_event():
    # DB engine a influx_client jsou inicializovány importem
    start_scheduler()