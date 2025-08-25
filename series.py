from logging import Logger
import logger as c_logger
import animeworld_scraper

logger: Logger = c_logger.my_logger(name="series_class")

class Series:
    def __init__(self, series: dict[str, str]) -> None:
        self.series_name: str = series["series_name"]
        self.season_num: str = series["season_num"]
        self.site_name: str = series["site_name"]
        self.download_url: str = series["download_url"]
        self.season_name: str = self.__get_season_name()
        self.num_of_ep: int = 0
    
    def __str__(self) -> str:
        return self.series_name
    
    def __get_season_name(self) -> str:
        match self.site_name:
            case "animeworld":
                name: str = self.download_url.split("play/")[1].split(".")[0]
                return name
            
            case _:
                return ""
            
    def get_ep_links(self) -> list[dict[str, str]] | None:
        match self.site_name:
            case "animeworld":
                return animeworld_scraper.animeworld_scraper(self.download_url)
            
            case _:
                return None
        