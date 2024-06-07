class Comment:
    def __init__(self, text, comment_id, video_id):
        self.text: str = text
        self.comment_id: str = comment_id
        self.video_id: str = video_id
        self.link: str = self.generate_link()
        self.type: int = 0

    def generate_link(self) -> str:
        return f'https://www.youtube.com/watch?v={self.video_id}&lc={self.comment_id}'

    def __str__(self):
        return f'Yorum: {self.text}\nLink: {self.link}\n'
    
    def to_dict(self):
        return {
            'text': self.text,
            'comment_id': self.comment_id,
            'video_id': self.video_id,
            'link': self.link,
            'type': int(self.type)
        }