import os
from dotenv import load_dotenv
from pymongo import MongoClient
from news_scrapper import NewsScrapper
from sentiment_analyzer import SentimentAnalyzer

load_dotenv()

# connect to DB
DB_URL = os.getenv("MONGO_URL")
client = MongoClient(DB_URL)
db = client[os.getenv("DB_NAME")]

# connect to news collection in the DB
news = db[os.getenv("NEWS_COLLECTION_NAME")]

# connect to users collection in the DB
news = db[os.getenv("NEWS_COLLECTION_NAME")]

def process_language_news(lang, scraper, analyzer):
    news_list = scraper.fetch_news(lang)
    for news in news_list:
        sentiment = analyzer.analyze_sentiment(news['title'], news['language'])
        news['tonality'] = sentiment['label']
        news['score'] = sentiment['score']
    return news_list

# initialize all models performing different activities in news collection 
def process_news():
    languages = ['en', 'hi', 'kn', 'te', 'bn', 'ml', 'mr']
    scraper = NewsScrapper()
    analyzer = SentimentAnalyzer()
    
    all_news = []

    for lang in languages:
        news_list = process_language_news(lang, scraper, analyzer)
        all_news.extend(news_list)
    news.insert_many(all_news)

def clear_news_collection():
    news.drop()

if __name__ == "__main__":
    clear_news_collection()
    process_news()
    print("News articles have been added to the database with sentiment analysis.")