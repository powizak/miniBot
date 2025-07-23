# InfluxDB – inicializace

## Základní nastavení

- Organizace: použijte hodnotu `${INFLUXDB_ORG}` z `.env`
- Bucket: použijte hodnotu `${INFLUXDB_BUCKET}` z `.env`
- Token: použijte hodnotu `${INFLUXDB_TOKEN}` z `.env`

## První spuštění

Při prvním spuštění kontejneru InfluxDB (docker-compose) se organizace a bucket vytvoří automaticky dle proměnných v `.env`.

## Struktura časových řad

- Doporučený measurement: `bot_metrics`
- Tagy: `bot_id`, `user_id`, `symbol`, `strategy`
- Fieldy: např. `balance`, `profit`, `drawdown`, `trade_count`, `custom_metric`
- Timestamp: automaticky

## Ruční vytvoření bucketu/organizace (CLI)

```
docker exec -it <influxdb_container> influx bucket create -n <bucket_name> -o <org_name> -t <token>
```

## Poznámka

Pro detailní návrh schématu časových řad doporučujeme řídit se konkrétními metrikami, které bude backend ukládat.