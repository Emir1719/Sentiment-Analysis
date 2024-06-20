import re
from nltk.tokenize import word_tokenize
from util.stopwords import StopWords

def clean_text(comment):
    # Küçük harfe çevirme
    comment = comment.lower()
    # Noktalama işaretlerini kaldırma
    comment = re.sub(r'[^\w\s]', '', comment)
    # Sayıları kaldırma
    comment = re.sub(r'\d+', '', comment)
    # Tokenize etme
    words = word_tokenize(comment)
    # Custom Stopwords
    stopwords = StopWords().turkishWords
    # Yazım hatalarını düzeltme ve stopwords kaldırma
    cleaned_words = [word if word else word for word in words if word not in stopwords]
    # Temizlenmiş kelimeleri birleştirme
    cleaned_comment = ' '.join(cleaned_words)
    
    return cleaned_comment