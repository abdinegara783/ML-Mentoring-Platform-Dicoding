from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Kode Mentee, Mentor, dan MentoringPlatform
# (termasuk kode pengolahan data mentee dan mentor)

# Membaca data mentor dari file CSV
df_mentor = pd.read_csv('C:/Users/Asus/pyton for data science/mentoring/df_mentor_fix1.csv')

# Inisialisasi Flask
app = Flask(__name__)
platform = MentoringPlatform()

# Route untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk penambahan mentee
@app.route('/add_mentee', methods=['POST'])
def add_mentee():
    name = request.form['name']
    needs = request.form['needs']
    mentee = Mentee(name, needs)
    platform.add_mentee(mentee)
    return "Mentee added successfully!"

# Fungsi untuk mencocokkan mentee dengan mentor
def match_mentee_with_mentor(mentee):
    matched_mentors = platform.find_mentor(mentee)
    if len(matched_mentors) > 0:
        result = f"Mentee '{mentee.name}' cocok dengan mentor:\n\n"
        for mentor, similarity_score in matched_mentors:
            mentor_info = df_mentor[df_mentor['name'] == mentor.name]
            mentor_id = mentor_info['ID'].values[0]
            mentor_job = mentor_info['Jobs'].values[0]
            mentor_rating = mentor_info['rating'].values[0]
            result += f"- ID    : {mentor_id}\n- Name   : {mentor.name}\n- Job    : {mentor_job}\n- Rating : {mentor_rating}\n\n"
        return result
    else:
        return f"Mentee '{mentee.name}' tidak ditemukan mentor yang cocok."

# Route untuk mencocokkan mentee dengan mentor
@app.route('/match_mentee', methods=['POST'])
def match_mentee():
    name = request.form['name']
    needs = request.form['needs']
    mentee = Mentee(name, needs)
    result = match_mentee_with_mentor(mentee)
    return result

# Menjalankan aplikasi Flask
if __name__ == '__main__':
    # Fitting vectorizer
    for index, row in df_mentor.iterrows():
        mentor_expertise = ' '.join(row['about'].split()[:10])  # Mengambil maksimal 10 kata dari mentor.expertise
        mentor = Mentor(row['name'], mentor_expertise, row['rating'])
        platform.add_mentor(mentor)
    platform.fit_vectorizer()

    app.run()

