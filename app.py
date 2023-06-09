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
@app.route("/matchmaking/<userId>", methods=["GET"])
def match_mentee(userId):
    fullName = request.args.get('fullName')
    needs = request.args.get('needs')
    platform = setMentorsInput(userId)
    result = platform.match_mentee_with_mentor(fullName, needs)
    result_encoded = list(map(lambda mentor: mentor.__dict__(), result))
    return jsonify({"status": "success", "mentors": result_encoded})


# Menjalankan aplikasi Flask
if __name__ == "__main__":
    # Fitting vectorizer
    app.run(port=5552)
