# TODO – Vývoj autonomního multi-strategického bota

## 1. Infrastruktura a základní prostředí
- [x] Vytvořit adresářovou strukturu projektu
- [x] Připravit `docker-compose.yml` a Dockerfile pro všechny služby
- [x] Připravit `.env` a bezpečné načítání klíčů

## 2. Backend (Core, FastAPI)
- [ ] Inicializovat FastAPI aplikaci
- [ ] Implementovat REST API pro správu botů
  - [x] Endpointy pro CRUD operace s instancemi botů
  - [x] Endpoint pro spuštění/pozastavení bota
  - [x] Endpoint pro manuální obchodování
- [x] Implementovat websocket pro real-time data
- [ ] Napojení na PostgreSQL (SQLAlchemy)
- [ ] Napojení na InfluxDB (influxdb-client)
- [ ] Implementovat plánovač úloh (APScheduler)
- [ ] Implementovat obchodní logiku a strategie
  - [x] Technické indikátory (RSI, MACD, BB, MA…)
  - [x] Řízení rizika (Stop-Loss, omezení pozic)
  - [x] Panic režim
- [x] Integrace ML modelu (LSTM/scikit-learn)
  - [x] Periodický retrénink
- [x] API wrapper pro Pionex (včetně ošetření chyb a rate limitů)
- [x] API wrapper pro Gemini (včetně retry s exponential backoff)
- [x] Logování a auditní stopa všech akcí

## 3. Frontend (React/Vue)
- [x] Inicializovat projekt (React/Vue)
- [x] Připravit autentizaci uživatele
- [x] Dashboard – přehled portfolia, P/L, stav botů
- [x] Správa botů (vytváření, konfigurace, spouštění, zastavování)
- [x] Historie obchodů a logů (filtrovatelný přehled)
- [x] Grafy a vizualizace (ECharts/TradingView)
- [x] Real-time notifikace

## 4. Databáze
- [ ] Inicializace PostgreSQL a InfluxDB
- [ ] Návrh schémat pro obě DB
- [ ] Migrace a inicializační skripty

## 5. Testování a nasazení
- [ ] Testy backendu (unit/integration)
- [ ] Testy frontendových komponent
- [ ] CI/CD pipeline (build, test, deploy)
- [ ] Dokumentace k nasazení a provozu
## Nedokončené části a placeholdery

- **backend/main.py**
  - Websocket endpoint `/ws/realtime` je pouze demo a neposkytuje reálná data.
    Úkol: Upravit websocket endpoint tak, aby poskytoval skutečná data z obchodování nebo databáze. [ ]

- **backend/api.py**
  - Chybí auditní logování CRUD operací s boty.
    Úkol: Přidat auditní logování všech akcí v API (vytvoření, úprava, smazání, spuštění, pozastavení bota). [ ]

- **backend/tests/test_main.py**
  - Testy pokrývají pouze root a 404, root endpoint není implementován, chybí testy na CRUD endpointy.
    Úkol: Opravit nebo doplnit testy backendu – pokrýt CRUD operace s boty a websocket. [ ]

- **.github/workflows/ci-cd.yml**
  - Sekce nasazení obsahuje pouze placeholder krok.
    Úkol: Doplnit reálné kroky pro nasazení (např. build, push Docker image, nasazení na server/cloud). [x]

- **frontend/README.md**
  - Obsahuje poznámku "placeholder" a chybí popis finální implementace.
    Úkol: Aktualizovat README s aktuálním stavem a návodem k použití frontendové aplikace. [x]

- **frontend/app/src/components/Auth.js**
  - Komponenta obsahuje pouze placeholder pro přihlášení.
    Úkol: Implementovat kompletní autentizaci uživatele (formulář, validace, komunikace s backendem, správa session/tokenu). [x]

- **frontend/app/src/components/BotsManager.js**
  - Komponenta obsahuje pouze seznam a akce jako placeholdery.
    Úkol: Implementovat správu botů – načítání seznamu, vytváření, konfiguraci, spouštění, zastavování a mazání botů s napojením na backend. [x]

- **frontend/app/src/components/Charts.js**
  - Komponenta obsahuje pouze placeholdery pro grafy.
    Úkol: Implementovat vizualizaci vývoje ceny, objemů, indikátorů a obchodů pomocí knihovny ECharts nebo TradingView, včetně napojení na data. [x]

- **frontend/app/src/components/Notifications.js**
  - Komponenta obsahuje pouze placeholder pro notifikace.
    Úkol: Implementovat real-time systém notifikací (příjem, zobrazení, mazání), napojení na websocket backendu. [x]

- **frontend/app/src/components/TradeHistory.js**
  - Komponenta obsahuje pouze placeholdery pro historii obchodů a logy.
    Úkol: Implementovat filtrovatelný přehled obchodů a logů s možností detailního zobrazení, napojení na backend.