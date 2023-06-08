from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from App.dicoding import Mentee, setMentorsInput
import json
import nltk

nltk.download("stopwords")
nltk.download("punkt")

# Inisialisasi Flask
app = Flask(__name__)


# Route untuk mencocokkan mentee dengan mentor
@app.route("/matchmaking", methods=["POST"])
def match_mentee():
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        json = request.get_json()
        platform = setMentorsInput(json["userId"])
        result = platform.match_mentee_with_mentor(json["fullName"], json["needs"])
        result_encoded = list(map(lambda mentor: mentor.__dict__(), result))
        return jsonify({"status": "success", "data": result_encoded})
    else:
        return "Content-Type not supported!"


# Menjalankan aplikasi Flask
if __name__ == "__main__":
    # Fitting vectorizer
    app.run()
