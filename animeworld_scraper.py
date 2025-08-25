import requests
from logging import Logger
import logger as c_logger
from bs4 import BeautifulSoup, Tag

# urllib3 è una testa di cazzo e manda warning per i certificati anche se gli dico di ignorarli (verify=False)
import urllib3
urllib3.disable_warnings()

logger: Logger = c_logger.my_logger(name="scraper")

def animeworld_scraper(url:str) -> list[dict[str, str]] | None:
    logger.info("Scraping started for Animeworld")
    episodes_url_list: list[str] | None = stage_1_animeworld_scraper(url)
    if episodes_url_list is None:
        return None
    
    episodes_list: list[dict[str, str]] = []
    ep_num: int = 1
    
    for episode_url in episodes_url_list:
        link: str | None = stage_2_animeworld_scraper(episode_url)
        if link is None:
            return None
        file_name: str = link.split("/")[-1].split(".")[0]
        
        episodes_list.append({
            "ep_name": file_name,
            "ep_number": str(ep_num),
            "download_link": link
        })
        ep_num += 1
    
    logger.info("Scraping ended for Animeworld")
    return episodes_list

def stage_1_animeworld_scraper(url:str) -> list[str] | None:
    headers: dict[str, str] = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    r: requests.Response = requests.get(url=url, headers=headers, verify=False)
    if r.status_code != 200:
        logger.error(f"Scrape failed, got {r.status_code}. Check page status")
        return None
        
    soup = BeautifulSoup(r.content, 'html5lib')

    episodes_tags_list = soup.find_all("li", attrs={"class":"episode"})

    episodes_download_links_list: list[str] = []
    uri: str = url.split("play/")[0]
    
    for tag in episodes_tags_list:
        try:
            assert isinstance(tag, Tag)
            assert isinstance(tag.a, Tag)
        
        except TypeError as error:
            logger.error(f"episodes_tags_list did not contained was not type Tag. Check the site for changes in HTML \n {error} \n")
            return None
        
        link: str = str(tag.a.get("href"))
        episodes_download_links_list.append(uri+link)
        
    
    #HTML page contains duplicate of links that have different url
    cleaned_links_list: list[str] = []
    for n in range(int(len(episodes_download_links_list)/2)):
        cleaned_links_list.append(episodes_download_links_list[n])
    
    return cleaned_links_list

def stage_2_animeworld_scraper(url:str) -> str | None:
    headers: dict[str, str] = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    r: requests.Response = requests.get(url=url, headers=headers, verify=False)
    if r.status_code != 200:
        logger.error(f"Scrape failed, got {r.status_code}. Check page status")
        return None
    
    soup = BeautifulSoup(r.content, 'html5lib')
    
    download_link = soup.find("a", attrs={"id":"alternativeDownloadLink"})

    try:
        assert isinstance(download_link, Tag)
        
    except AssertionError as error:
        logger.error(f"Stage 2 scraper did not returned Type Tag. Check the site for changes in HTML /n {error} /n")
        return None
    
    clean_download_link = str(download_link.get("href"))
    
    return clean_download_link


if __name__ == "__main__":
    # x = animeworld_scraper("https://www.animeworld.ac/play/watari-kun-no-xx-ga-houkai-sunzen.171gF/7sr4XB")
    # print(x)
    pass