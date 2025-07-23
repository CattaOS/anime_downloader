import requests
from logging import Logger
import logger as c_logger

logger: Logger = c_logger.my_logger(name="downloader")

def downloader(url: str, file_name: str) -> bool:
    logger.info(f"Download started for {file_name}")
    r = requests.get(url=url, stream = True)
    if r.status_code != 200:
        logger.error(f"Download failed, got {r.status_code}. Check page status")
        return False
    
    with open(f"{file_name}.mp4","wb") as mp4:
        for chunk in r.iter_content(chunk_size=1024*1024):
            if chunk:
                mp4.write(chunk)
    logger.info(f"Download ended for {file_name}")
    return True