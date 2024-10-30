from dotenv import load_dotenv
from os import getenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=getenv("GEMINI_API_KEY"))

def news_content_elaborator(news_title):
    iniPrompt = ("You are a news elaborator for Indian news, take the news and output 3 lines of content for the news not more than 30 words and without any text formatting, punctuations.")
    query = iniPrompt + news_title
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(query)

    if response and response.candidates:
        for candidate in response.candidates:
            if any(rating.category == "blocked" for rating in candidate.safety_ratings):
                return "Content cannot be provided due to safety concerns."
            if candidate.content.parts.__len__() == 0:
                return "Content cannot be provided due to safety concerns."
            return candidate.content.parts[0].text
        
# testing
# print(news_content_elaborator("India launches new satellite for weather monitoring"))