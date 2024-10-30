from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from department_classification import dept_classifier
from time import sleep
from news_content_elaborator import news_content_elaborator

load_dotenv()

class NewsScrapper:
    def __init__(self):
        self.base_url = "https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNRE55YXpBU0JXVnVMVWRDS0FBUAE?hl=en-IN&gl=IN&ceid=IN%3A"

    def fetch_news(self, lang):
        newslist = []
        r = requests.get(self.base_url + lang)
        htmlContent = r.content
        soup = BeautifulSoup(htmlContent, 'html.parser')
        articles = soup.find_all("article", class_="IBr9hb")
        anchors = []
        for article in articles[:20]:
            anchors.append(article.find(attrs={'class':'gPFEn'}))

        images = soup.find_all("img", class_="Quavad")[:20]
        for link, image in zip(anchors, images):
            title = link.text
            newslink = "https://news.google.com"+link.get('href')[1:]
            imglink = image.get('srcset')
            imglink = imglink.split("1x")[0]

            # dept classification
            department = dept_classifier(title)
            sleep(5)

            # news elaboration
            content = news_content_elaborator(title)
            sleep(5)

            newsarticle = {
                'title': title,
                'link': newslink,
                'img': imglink,
                'content': content,
                'language': lang,
                'department': department,
                'source': 'Google News Website',
                'publicationDate': datetime.now(),
            }
            newslist.append(newsarticle)
        return newslist