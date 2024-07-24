import joblib
from util.comment import Comment
from util.clean_data import clean_text
from util.svc_model import SvcModel

def predictSentiment(comment: str, model, vectorizer):
    """
    Duygu analizi yapıp ilgili kategorinin sayısal değrini döndürür.

    Args:
        comment: Yorumun metni

    Returns:
        int: The predicted sentiment category's numerical value (may vary depending on your model's output).
    """
    try:
        data = clean_text(comment)
        comment_vectorized = vectorizer.transform([data.lower()])
        prediction = model.predict(comment_vectorized)[0]  # Extract first element of prediction array
        return prediction

    except FileNotFoundError:
        print("Model ile ilgili dosyalar bulunamadı.")
        return None  # Or raise a custom exception if preferred

    except (joblib.exceptions.JoblibError, AttributeError) as e:
        print(f"Model yüklenirken bir hata oluştu: {e}")
        return None

    except ValueError as e:
        print(f"Yorum bir metin olmalı. Error: {e}")
        return None
    

def classifyComments(comments: list[Comment]):
    """
    Tüm yorumları sınıflandırır.
    """
    model = SvcModel()
    model.load_model("model/model.pkl")

    for comment in comments:
        comment.type = model.predict(comment.text)


def getCommentsByType(comments: list[Comment], type: int = 0):
    """
    Parametre olarak verilen `type` değerine ait yorumları döndürür.

    Args:
        type: Filtrelemede kullanılacak yorum türü.

    Returns:
        Liste: Belirtilen `type` değerine sahip tüm yorumlar.
    """
    return [comment.to_dict() for comment in comments if comment.type == type]