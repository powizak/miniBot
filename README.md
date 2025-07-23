# Autonomní multi-strategický obchodní bot pro kryptoměnové burzy

## Struktura projektu

```
miniBot/
├── backend/              # Core Backend (Python, FastAPI)
├── frontend/             # Webové rozhraní (React/Vue)
├── db/
│   ├── influxdb/         # InfluxDB data/config
│   └── postgres/         # PostgreSQL data/config
├── docker-compose.yml    # Definice služeb
├── .env.example          # Ukázka konfiguračních proměnných
└── README.md             # Tento soubor
```

## Rychlý start

1. Zkopírujte `.env.example` na `.env` a doplňte citlivé údaje.
2. Spusťte `docker-compose up -d`
3. Přístup k UI: http://localhost:${FRONTEND_PORT}

## Komponenty

- **backend/** – FastAPI, obchodní logika, API wrappery, ML
- **frontend/** – React/Vue, dashboard, správa botů
- **db/influxdb/** – časové řady
- **db/postgres/** – konfigurace, logy, historie obchodů

## Bezpečnost

- API klíče a citlivá data pouze v `.env` nebo Docker secrets.
- Přístup k UI chráněn autentizací.

## Poznámky

- Veškeré služby běží v kontejnerech (Docker Compose).
- Další dokumentace v příslušných složkách.