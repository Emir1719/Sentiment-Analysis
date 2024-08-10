from util.comment import Comment
from util.svc_model import SvcModel

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