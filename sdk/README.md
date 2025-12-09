# Zestaw SDK swcpy
To jest zestaw SDK dla Pythona do interakcji z interfejsem API SportsWorldCentral
Football, stworzonym na potrzeby książki [Interfejsy API w AI i Data
Science](https://handsonapibook.com).

## Instalacja swcpy
Aby zainstalować ten zestaw SDK w swoim środowisku, należy wykonać następujące
polecenie:
`pip install swcpy@git+https://github.com/dave-m91/projekt-portfolio#
subdirectory=sdk`

## Przykład użycia
To SDK implementuje wszystkie punkty końcowe API SWC, a dodatkowo umożliwia pobieranie
pełnych zbiorów danych fantasy SWC w formacie CSV.

### Ustawianie podstawowego adresu URL dla API
SDK szuka w zmiennych środowiskowych wartości `SWC_API_BASE_URL`. Zalecaną metodą
ustawienia podstawowego adresu URL dla API SWC jest utworzenie w katalogu projektu pliku
`.env` z następującą zawartością::
```
SWC_API_BASE_URL={URL Twojego API}
```
Możesz również ustawić tę wartość jako zmienną środowiskową w środowisku, w którym
używasz SDK, lub przekazać ją jako parametr do metody `SWCConfig()`.

### Przykład użycia standardowych funkcji API
Oto przykład wywołania funkcji SDK dla standardowych punktów końcowych API:
```python
from swcpy import SWCClient
from swcpy import SWCConfig
config = SWCConfig(swc_base_url="http://0.0.0.0:8000",backoff=False)
client = SWCClient(config)
leagues_response = client.list_leagues()
print(leagues_response)
```
### Przykład użycia funkcji do pobierania pełnych plików danych
Punkt końcowy do pobierania pełnych plików danych zwraca obiekt bytes. Oto przykład
zapisywania w lokalnym systemie plików danych z punktu końcowego pobierania pełnych
plików danych:
```python
import csv
import os
from io import StringIO
config = SWCConfig()
client = SWCClient(config)
"""Testy pobierania pełnego pliku danych o zawodnikach z użyciem SDK"""
player_file = client.get_bulk_player_file()

# Zapis pliku na dysku w celu weryfikacji jego pobrania
output_file_path = data_dir + 'players_file.csv'
with open(output_file_path, 'wb') as f:
f.write(player_file)
```