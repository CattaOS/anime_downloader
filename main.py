from logging import Logger
import logger as c_logger
import scrapers
import downloader
import os

logger: Logger = c_logger.my_logger(name="ADA")
download_folder = "C:\\Users\\CattaOS\\Videos\\"

def main() -> None:
    url: str = input("Insert series url:")
    link_and_file_name_list: list[list[str]] | None = []
    
    match url:
        case x if "animeworld" in url:
            print("Started scraping")
            link_and_file_name_list = scrapers.animeworld_scraper(url)
            
            if link_and_file_name_list is None:
                print("There were problem with the scraper, check the logs")
                return
            
            folder_name: str = url.split("play/")[1].split(".")[0]

        case _:
            print("No scraper for the given url")
            return
    
    try:
        os.mkdir(download_folder + folder_name)
        print(f"Directory '{folder_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{folder_name}' already exists.")
    
    folder: str = download_folder + folder_name
    
    for link_and_file_name in link_and_file_name_list:
        file_name: str = folder + "\\" + link_and_file_name[1]
        if os.path.isfile(file_name):
            print(f"{link_and_file_name[1]} already downloaded, skipping.")
            continue
        
        print(f"Download started for {link_and_file_name[1]}")
        ok_status: bool = downloader.downloader(link_and_file_name[0], file_name)
        
        if not ok_status:
            print(f"There were problem with the download for {link_and_file_name[1]}, check the logs")
            return
        
        print(f"Download ended for {link_and_file_name[1]}")


if __name__ == "__main__":
    lol = main()