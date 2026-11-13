# Laboratorium 6 - XSS (rozwiązanie)

Poprawiona aplikacja "Tablica ogłoszeń" z laboratorium 6.

## Uruchomienie

```
docker compose up -d --build
```

Aplikacja: http://127.0.0.1:8080
Zbieracz:  http://localhost:8081

Po zmianie kodu: `docker compose restart web`.
Logi: `docker compose logs --tail 30 web`, `docker compose logs zbieracz`.
Zatrzymanie: `docker compose down`.

Konta: `anna` / `anna-lab6`, `student` / `student-lab6`.

## Wprowadzone poprawki

| Zadanie | Plik | Zmiana |
|---|---|---|
| 1 | `aplikacja/app.py:37` | `escape(fraza)` - kodowanie parametru `q` |
| 2 | `aplikacja/app.py:10` | `SESSION_COOKIE_HTTPONLY = True` |
| 3 | `aplikacja/templates/tablica.html` | usunięty filtr `\|safe` |
| 3 | `aplikacja/templates/podglad.html` + `static/podglad.js` | `innerHTML` -> `textContent`, skrypt w osobnym pliku |
| 3 | `aplikacja/app.py` (`@app.after_request`) | nagłówek Content-Security-Policy |

Wyniki i ładunki: `raport.txt`.
