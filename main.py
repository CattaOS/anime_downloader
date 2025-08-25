from logging import Logger
import logger as c_logger
import downloader
from series import Series
from utils import FileIO
import os

logger: Logger = c_logger.my_logger(name="ADA")
usr: str = os.getlogin()
download_folder = "/media/Jellifyn/Anime/"


def get_ani_list() -> list[dict[str, str]] | None:
    ani_list = FileIO.read_json("download_list.json")
    
    try:
        assert isinstance(ani_list, list)
        
    except TypeError:
        logger.error("anime list json not formatted properly.\n Expected `list`, got `dict`")
        return None
    
    return ani_list

def main() -> None:
    anime_list: list[dict[str, str]] | None = get_ani_list()
    
    if anime_list is None:
        return
    anime_list.pop(0)
    anime_list: list[Series] = list(map(lambda x : Series(x), anime_list))
    
    logger.info("Download block start.")
    
    for anime in anime_list:
        try:
            os.mkdir(download_folder + anime.series_name)
            logger.info(f"Directory '{anime.series_name}' created successfully.")
            
        except FileExistsError:
            logger.info(f"Directory '{anime.series_name}' already exists.")
        
        folder_name: str = anime.series_name + f"/Season {anime.season_num}"
        try:
            os.mkdir(download_folder + folder_name)
            logger.info(f"Directory '{folder_name}' created successfully.")
            
        except FileExistsError:
            logger.info(f"Directory '{folder_name}' already exists.")

        ep_links_list: list[dict[str, str]] | None = anime.get_ep_links()
        
        if ep_links_list is None:
            continue
        
        for ep_links in ep_links_list:
            file_name: str = download_folder + folder_name + "/" + ep_links["ep_name"]
    
            if os.path.isfile(file_name):
                print(f"{ep_links["ep_name"]} already downloaded, skipping.")
                continue
            
            logger.info(f"Download started for {ep_links["ep_name"]}")
            ok_status: bool = downloader.downloader(ep_links["download_link"], file_name)
        
            if not ok_status:
                logger.warning(f"There were problem with the download for {ep_links["ep_name"]}, check the logs")
    
    logger.info("Download block end.\n\n")


if __name__ == "__main__":
    lol: None = main()