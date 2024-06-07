from typing import List
from googleapiclient.discovery import build
from util.comment import Comment
import os

def getAllCommentsV3(urls: list) -> List[Comment]:
    """
    Verilen YouTube linklerindeki yorumları getirir ve Comment sınıfı ile temsil eder.
    Hem ana akışdaki (top-level) yorumu hem de yorumlara verilen yanıtları da getirir.
    """
    
    # YouTube API connection
    api_key = os.getenv("YoutubeApiKey")
    youtube = build('youtube', 'v3', developerKey=api_key)

    all_comments = []
    
    for url in urls:
        if "shorts" in url:
            video_id = url.split("/")[-1]
        else:
            video_id = url.split("v=")[1].split("&")[0]

        next_page_token = None

        while True:
            results = youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_id,
                textFormat='plainText',
                pageToken=next_page_token,
                maxResults=100  # Maximum number of comments to retrieve per page
            ).execute()

            for item in results['items']:
                comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comment_id = item['snippet']['topLevelComment']['id']
                top_level_comment = Comment(comment_text, comment_id, video_id)
                all_comments.append(top_level_comment)
                
                # Check if there are replies to the top-level comment
                if 'replies' in item:
                    for reply in item['replies']['comments']:
                        reply_text = reply['snippet']['textDisplay']
                        reply_id = reply['id']
                        reply_comment = Comment(reply_text, reply_id, video_id)
                        all_comments.append(reply_comment)

            next_page_token = results.get('nextPageToken')

            if not next_page_token:
                break

    return all_comments  # Return all comments