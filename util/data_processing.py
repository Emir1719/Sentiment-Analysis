import re
from util.stopwords import StopWords
from util.correct_word import dictionary
from nltk.tokenize import word_tokenize
from nltk import WordNetLemmatizer

class DataProcessing:
    def __init__(self):
        self.stopwords = StopWords().turkishWords
        self.lemma = WordNetLemmatizer()
    
    # Temizleme ve yazım hatası düzeltme fonksiyonu
    def clean_text(self, comment):
        comment = comment.lower()
        comment = re.sub(r'[^\w\s]', '', comment)
        comment = re.sub(r'\d+', '', comment)
        words = word_tokenize(comment)
        cleaned_words = [dictionary.get(word, word) for word in words if word not in self.stopwords]
        cleaned_comment = ' '.join(cleaned_words)
        return cleaned_comment

    def pre_processing(self, text):
        text = text.lower()  #Büyük harften -Küçük harfe çevirme
        text = re.sub("[^abcçdefgğhıijklmnoöprsştuüvyz]"," ",text)
        text = word_tokenize(text) # splits the words that are in the sentence from each other.
        text = [word for word in text if not word in set(self.stopwords)]
        text = [self.lemma.lemmatize(word) for word in text] # this code finds the root of the word for a word in the sentence and change them to their root form.
        text = " ".join(text)
        return text