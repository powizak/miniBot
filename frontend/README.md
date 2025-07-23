# Frontend miniBot

Webové rozhraní pro správu a monitoring autonomních obchodních botů. Postaveno na React.js.

## Funkce

- **Přihlášení uživatele** (autentizace, správa session/tokenu)
- **Dashboard** – přehled portfolia, P/L, stav botů
- **Správa botů** – vytváření, konfigurace, spouštění, zastavování, mazání
- **Historie obchodů a logů** – filtrovatelný přehled s možností detailního zobrazení
- **Grafy a vizualizace** – vývoj ceny, objemů, indikátorů a obchodů (ECharts/TradingView)
- **Real-time notifikace** – příjem, zobrazení, mazání (websocket napojení na backend)

## Požadavky

- Node.js 20+
- npm

## Lokální spuštění

```bash
cd frontend/app
npm install
npm start
```

Aplikace poběží na [http://localhost:${FRONTEND_PORT}](http://localhost:${FRONTEND_PORT}).

## Build pro produkci

```bash
cd frontend/app
npm run build
```

## Konfigurace

- API endpointy jsou nastaveny v kódu nebo pomocí `.env` souboru v `frontend/app`.
- Pro správnou funkčnost je nutné mít spuštěný backend server (`FastAPI`).

## Autentizace

- Přihlášení uživatele probíhá přes formulář, token je uložen v localStorage/session.
- Všechny chráněné akce vyžadují platný token.

## Poznámky

- Pro správné napojení na backend upravte URL v kódu nebo v `.env`.
- Pro websocket notifikace je potřeba mít backend spuštěný s podporou websocketů.