import os
from dotenv import load_dotenv
load_dotenv()

class SWCConfig:
    '''Klasa konfiguracji zawierająca argumenty dla SDK'''
    swc_base_url: str
    swc_backoff: bool
    swc_backoff_max_time: int
    swc_bulk_file_format: str
    def __init__(
            self,
            swc_base_url: str = None,
            backoff: bool = True,
            backoff_max_time: int = 30,
            bulk_file_format: str = "csv"
    ):
        '''Konstruktor dla klasy konfiguracji
        Args:
        swc_base_url (optional): Podstawowy adres url dla wywołań API
        Pozostałe argumenty...'''
        self.swc_base_url = swc_base_url or os.getenv("SWC_API_BASE_URL")
        print(f"SWC_API_BASE_URL w konstruktorze SWCConfig: {self.swc_base_url}")
        if not self.swc_base_url:
            raise ValueError("Wymagany podstawowy adres URL. Ustaw zmienną środowiskową SWC_API_BASE_URL")
        self.swc_backoff = backoff
        self.swc_backoff_max_time = backoff_max_time
        self.swc_bulk_file_format = bulk_file_format
    def __str__(self):
        '''Funkcja zwracająca reprezentację tekstową  obiektu config'''
        return f"{self.swc_base_url} {self.swc_backoff} {self.swc_backoff_max_time} {self.swc_bulk_file_format}"
