# Ping Logger Add-on for Home Assistant (v0.2.6)

## Features
- Pinguje wybrane adresy IP w wybranym interwale
- Wysyła sensory do Home Assistant przez MQTT Discovery (jeden sensor per adres IP)
- Loguje wyniki pingów do CSV (z automatycznym czyszczeniem po X dniach)
- Pełna edycja ustawień przez GUI Supervisor Addon
- Oparty na Pythonie (działa na każdej platformie Home Assistant)

## Instalacja
1. Skopiuj katalog `ping_logger` do swojego repozytorium z dodatkami Home Assistant
2. Podmień pliki `Dockerfile`, `config.json`, `ping_logger.py`
3. Odśwież repozytoria dodatków w Home Assistant
4. Zainstaluj dodatek przez GUI
5. Skonfiguruj adresy IP, interwał, MQTT (login/hasło jeśli potrzeba) i uruchom

## Pliki
- Dockerfile – uniwersalny, wspiera wszystkie architektury
- config.json – konfiguracja, schema, architektury
- ping_logger.py – logika pingu i komunikacji przez MQTT

---

## Najczęstsze problemy
- Jeśli nie widzisz encji w HA: zrestartuj Home Assistant Core i sprawdź, czy MQTT Discovery jest aktywne
- Jeśli broker wymaga loginu/hasła – ustaw je w konfiguracji addonu i w Mosquitto
- Dodatek działa na Pythonie – nie wymaga żadnych obrazów z GHCR czy specjalnych baz

---

**Projekt: Waldzio / ChatGPT 2025**
