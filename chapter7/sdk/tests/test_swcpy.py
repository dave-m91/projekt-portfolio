import pytest
from swcpy.swc_client import SWCClient
from swcpy.swc_config import SWCConfig
from swcpy.schemas import League, Team, Player, Performance
from io import BytesIO
import pyarrow.parquet as pq
import pandas as pd

def test_health_check():
    """Test sprawdzający kondycje SDK"""
    config = SWCConfig(swc_base_url="http://0.0.0.0:8000", backoff=False)
    client = SWCClient(config)
    response = client.get_health_check()
    assert response.status_code == 200
    assert response.json()== {"message": "API health check successful"}

def test_list_league():
    """Testy pobierania listy lig"""
    config = SWCConfig(swc_base_url="http://0.0.0.0:8000", backoff=False)
    client = SWCClient(config)
    leagues_response = client.list_leagues()
    
    assert isinstance(leagues_response, list)

    for league in leagues_response:
        assert isinstance(league, League)
    assert len(leagues_response) == 5

def test_bulk_player_file_parquet():
    """Test pobierania plików do formatu parquet"""
    config = SWCConfig(bulk_file_format="parquet")
    client = SWCClient(config)

    player_file_parquet = client.get_bulk_player_file()
    player_table = pq.read_table(BytesIO(player_file_parquet))
    player_df = player_table.to_pandas()
    assert len(player_df) == 1018
