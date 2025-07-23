import os
import time
import threading
from collections import deque
import requests
from typing import Any, Dict, Optional, List, Callable
from requests.exceptions import RequestException, HTTPError

class PionexAPIError(Exception):
    pass

class PionexRateLimitError(PionexAPIError):
    pass

class PionexAPI:
    BASE_URL = "https://api.pionex.com"
    MAX_RETRIES = 5
    BACKOFF_FACTOR = 2

    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        self.api_key = api_key or os.getenv("PIONEX_API_KEY")
        self.api_secret = api_secret or os.getenv("PIONEX_API_SECRET")
        if not self.api_key or not self.api_secret:
            raise ValueError("Pionex API klíče nejsou nastaveny.")
        # Rate limiting: max 10 requests per second, else wait 10s
        self._rate_lock = threading.Lock()
        self._rate_timestamps = deque()
        self._rate_limit = 10
        self._rate_window = 1  # vteřina
        self._rate_wait = 10   # sekund

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        # Rate limiting
        with self._rate_lock:
            now = time.time()
            # Odstraň staré záznamy mimo okno
            while self._rate_timestamps and now - self._rate_timestamps[0] > self._rate_window:
                self._rate_timestamps.popleft()
            if len(self._rate_timestamps) >= self._rate_limit:
                # Pokud je limit dosažen, čekej 10 sekund
                time.sleep(self._rate_wait)
                # Po čekání znovu zkontroluj a vyčisti frontu
                now = time.time()
                while self._rate_timestamps and now - self._rate_timestamps[0] > self._rate_window:
                    self._rate_timestamps.popleft()
            self._rate_timestamps.append(time.time())

        url = f"{self.BASE_URL}{endpoint}"
        retries = 0
        delay = 1
        while retries < self.MAX_RETRIES:
            try:
                resp = requests.request(method, url, headers=self._headers(), timeout=10, **kwargs)
                if resp.status_code == 429:
                    raise PionexRateLimitError("Rate limit exceeded")
                resp.raise_for_status()
                return resp.json()
            except PionexRateLimitError:
                time.sleep(delay)
                delay *= self.BACKOFF_FACTOR
                retries += 1
            except (RequestException, HTTPError) as e:
                if retries >= self.MAX_RETRIES - 1:
                    raise PionexAPIError(f"Chyba komunikace s Pionex API: {e}")
                time.sleep(delay)
                delay *= self.BACKOFF_FACTOR
                retries += 1
        raise PionexAPIError("Maximální počet pokusů o komunikaci s Pionex API byl vyčerpán.")

    # --- Veřejné metody pro obchodní logiku ---

    def get_account(self) -> Dict[str, Any]:
        """Získá informace o účtu."""
        return self._request("GET", "/api/v1/account")

    def get_orders(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        """Získá seznam objednávek (volitelně pro konkrétní symbol)."""
        params = {"symbol": symbol} if symbol else {}
        return self._request("GET", "/api/v1/orders", params=params)

    def place_order(self, symbol: str, side: str, price: float, quantity: float, type_: str = "LIMIT") -> Dict[str, Any]:
        """Vytvoří novou objednávku."""
        data = {
            "symbol": symbol,
            "side": side,
            "price": price,
            "quantity": quantity,
            "type": type_
        }
        return self._request("POST", "/api/v1/orders", json=data)

    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """Zruší objednávku podle ID."""
        return self._request("DELETE", f"/api/v1/orders/{order_id}")

    def get_balance(self) -> Dict[str, Any]:
        """Získá zůstatky na účtu."""
        return self._request("GET", "/api/v1/account/balance")

    def get_order(self, order_id: str) -> Dict[str, Any]:
        """Získá detail objednávky podle ID."""
        return self._request("GET", f"/api/v1/orders/{order_id}")

    def get_order_by_client_id(self, client_order_id: str) -> Dict[str, Any]:
        """Získá detail objednávky podle client_order_id."""
        return self._request("GET", f"/api/v1/orders/client-order-id/{client_order_id}")

    def get_open_orders(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        """Získá otevřené objednávky (volitelně pro symbol)."""
        params = {"symbol": symbol} if symbol else {}
        return self._request("GET", "/api/v1/openOrders", params=params)

    def get_all_orders(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        """Získá všechny objednávky (volitelně pro symbol)."""
        params = {"symbol": symbol} if symbol else {}
        return self._request("GET", "/api/v1/allOrders", params=params)

    def get_fills(self, order_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Získá fill (provedené obchody) pro objednávku nebo všechny."""
        params = {"orderId": order_id} if order_id else {}
        return self._request("GET", "/api/v1/fills", params=params)

    def cancel_all_orders(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """Zruší všechny otevřené objednávky (volitelně pro symbol)."""
        params = {"symbol": symbol} if symbol else {}
        return self._request("DELETE", "/api/v1/orders", params=params)

    def get_market_trades(self, symbol: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Získá poslední obchody pro symbol."""
        params = {"symbol": symbol, "limit": limit}
        return self._request("GET", "/api/v1/trades", params=params)

    def get_market_depth(self, symbol: str, limit: int = 20) -> Dict[str, Any]:
        """Získá hloubku trhu (order book) pro symbol."""
        params = {"symbol": symbol, "limit": limit}
        return self._request("GET", "/api/v1/depth", params=params)

    def get_ticker_24hr(self, symbol: str) -> Dict[str, Any]:
        """Získá 24h ticker pro symbol."""
        params = {"symbol": symbol}
        return self._request("GET", "/api/v1/ticker/24hr", params=params)

    def get_book_ticker(self, symbol: str) -> Dict[str, Any]:
        """Získá nejlepší bid/ask pro symbol."""
        params = {"symbol": symbol}
        return self._request("GET", "/api/v1/ticker/bookTicker", params=params)

    def get_klines(self, symbol: str, interval: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Získá historická OHLCV data (klíny) pro symbol."""
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        return self._request("GET", "/api/v1/klines", params=params)