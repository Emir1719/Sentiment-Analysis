from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from util.youtube_comment import getAllCommentsV2
from util.sentiment import classifyComments, getCommentsByType
from dotenv import load_dotenv
load_dotenv()

# http://127.0.0.1:5000/
app = Flask(__name__)
CORS(app)  # CORS'u etkinleştir

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    urls = request.form['url'].split(',')
    comments = getAllCommentsV2(urls)
    print(f"Fetched {len(comments)} comments")  # Yorum sayısını yazdır

    classifyComments(comments)
    print("Comments classified")  # Sınıflandırmanın bittiğini yazdır
    
    response_data = {
        'all_comments': [comment.to_dict() for comment in comments],
        #'neutral_comments': getCommentsByType(comments, 0),
        'positive_comments': getCommentsByType(comments, 1),
        'criticism_comments': getCommentsByType(comments, 2),
        'donation_comments': getCommentsByType(comments, 3),
        #'negative_comments': getCommentsByType(comments, 4),
    }
    # print(f"Response data: {response_data}")  # Yanıt verilerini yazdır

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
