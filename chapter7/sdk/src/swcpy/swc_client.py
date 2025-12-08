import httpx
import swcpy.swc_config as config

from .schemas import League, Team, Player, Performance
from typing import List
import backoff
import logging

logger = logging.getLogger(__name__)

class SWCClient:
    """Interakcja z SWC API
    SDK ułatwia proces uytkownia SWC Fantasy Football API
    Przykładowe uzycie:
    client = SWCClient()
    response = client.get_health_check()"""

    HEALTH_CHECK_ENDPOINT = "/"
    LIST_LEAGUES_ENDPOINT = "/v0/leagues/"
    LIST_PLAYERS_ENDPOINT = "/v0/players/"
    LIST_PERFORMANCES_ENDPOINT = "/v0/performances/"
    LIST_TEAMS_ENDPOINT = "/v0/teams/"
    GET_COUNTS_ENDPOINT = "/v0/counts/"
    BULK_FILE_BASE_URL = (
        "https://raw.githubusercontent.com/dave-m91/projekt-portfolio/main/bulk/"
    )
    def __init__(self, input_config: config.SWCConfig):
        logger.debug(f"Bulk file base URL: {self.BULK_FILE_BASE_URL}")
        logger.debug(f"Input config: {input_config}")
        self.swc_base_url = input_config.swc_base_url
        self.backoff = input_config.swc_backoff
        self.backoff_max_time = input_config.swc_backoff_max_time
        self.bulk_file_format = input_config.swc_bulk_file_format
        self.BULK_FILE_NAMES = {
            "players": "player_data",
            "leagues": "league_data",
            "performances": "performance_data",
            "teams": "teams_data",
            "team_player": "team_player_data"
        }
        if self.backoff:
            self.call_api = backoff.on_exception(
                wait_gen=backoff.expo,
                exception=(httpx.RequestError, httpx.HTTPStatusError),
                max_time = self.backoff_max_time,
                jitter=backoff.random_jitter,
            )(self.call_api)
        if self.bulk_file_format.lower() == "parquet":
            self.BULK_FILE_NAMES = {
                key: value + ".parquet" for key, value in self.BULK_FILE_NAMES.items()
            }
        else:
            self.BULK_FILE_NAMES = {
                key: value + ".csv" for key, value in self.BULK_FILE_NAMES.items()
            }
        logger.debug(f"Bulk file dictionary: {self.BULK_FILE_NAMES}")

def call_api(self,
             api_endpoint: str,
             api_params: dict = None) -> httpx.Response:
    """Make API call and logs errors."""
    if api_params:
        api_params = {key: val for key, val in api_params.items()
                      if val is not None}
        
        try:
            with httpx.Client(base_url = self.swc_base_url) as client:
                logger.debug(f"base_url: {self.swc_base_url}, api_endpoint:\
                             {api_endpoint}, api_params: {api_params}")
                response = client.get(api_endpoint, params=api_params)
                logger.debug(f"Respponse JSON: {response.json()}")
                return response
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP status error occurred: {e.response.status_code}\
                         {e.response.text}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Request error occurred: {str(e)}")
            raise

def get_health_chec(self) -> httpx.Response:
    """Sprawdza, czy intefejs API działa
    
    Returns:
        Obiekt httpx.Response zawierający starus HTTP, odpowiedź JSON
        i inne informacje"""
    
    logger.debu("Sprawdzanie stanu działania API")
    endpoint_url = self.HEALTH_CHECK_ENDPOINT
    return self.call_api(endpoint_url)

def list_leagues(
        self,
        skip: int = 0,
        limit: int = 100,
        minimum_last_changed_date: str = None,
        league_name: str = None
) -> list[League]:
    """Zwraca listę lig przefiltrowaną według parametrów.
    Wywołuje punkt końcowy API v0/leagues i zwraca listę obiektów League.
    Returns:
    Lista obiektów schemas.League objects. Każdy reprezentuje jedną
    ligę fantasy SportsWorldCentral."""

    logger.debug("Pobieranie listy lig")

    params = {
        "skip": skip,
        "limit": limit,
        "minimum_last_changed_date" : minimum_last_changed_date,
        "league_name": league_name
    }
    response = self.call_api(self.LIST_LEAGUES_ENDPOINT, params)
    return [League(**league) for league in response.json()]

def get_bulk_player_file(self) -> bytes:
    """Zwraca plik z danymi użytkowników"""
    logger.debug("Uruchomiono metodę pobrania pliku zawodników")
    player_file_path = self.BULK_FILE_BASE_URL + self.BULK_FILE_NAMES["players"]
    response = httpx.get(player_file_path, follow_redirects=True)
    if response.staus_code == 200:
        logger.debug("Plik pobrano prawidłowo")
        return response.content