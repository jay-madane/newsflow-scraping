from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from easygoogletranslate import EasyGoogleTranslate

class SentimentAnalyzer:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
        self.model = AutoModelForSequenceClassification.from_pretrained("mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
        self.pipe = pipeline("sentiment-analysis", model=self.model, tokenizer=self.tokenizer)
        self.translator = EasyGoogleTranslate(
            target_language='en',
            source_language='auto',
            timeout=25
        )

    def analyze_sentiment(self, text, src_lang):
        if src_lang != 'en':
            translated_text = self.translator.translate(text)
        else:
            translated_text = text
        result = self.pipe(translated_text)[0]
        return {
            'label': result['label'].lower(),
            'score': result['score']
        }