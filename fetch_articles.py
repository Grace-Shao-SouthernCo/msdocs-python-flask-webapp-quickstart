import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_article_links(query, num_articles=5):
    base_url = "https://www.bing.com"
    url = f"{base_url}/news/search?q={query}"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.find_all("div", class_="t_s")
    mainBody = soup.find_all("main")
    mainImgs = []
    for main in mainBody:
        mainImgs.append(main.find_all("img")[1])

    article_links = []
    for article in articles:
        try:
            url = article.find("a", class_="title")["href"]
            title = article.find("a", class_="title").text
            parsed_url = urlparse(url)
            netloc_parts = parsed_url.netloc.split(".", 2)
            if len(netloc_parts) == 2:
                main_host = netloc_parts[0].capitalize()
            else:
                main_host = netloc_parts[1].capitalize()
            article_links.append({
                'title': title,
                'main_host': main_host,
                'url': url,
                'summary': None
            })
        except Exception as e:
            print(f"Error occurred while processing article: {e}")
    return article_links[:num_articles]