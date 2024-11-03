from dotenv import load_dotenv
from os import getenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=getenv("GEMINI_API_KEY"))

def dept_classifier(news_title):
    iniPrompt = ("You are a news department classifier for Indian news, take the news and output only the department without any text formatting, punctuations and use lowercase only. List of departments: sports, healthcare, business, politics, law, entertainment, weather, technology.")
    query = iniPrompt + news_title
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        response = model.generate_content(query)
        if response and response.candidates:
            return response.candidates[0].content.parts[0].text
        else:
            return "controversial"
    except Exception as e:
        print(f"Error during classification: {e}")
        return "controversial"

# testing
# print(dept_classifier("PM Modi arrives in Delhi after concluding two-nation visit to Russia a…"))