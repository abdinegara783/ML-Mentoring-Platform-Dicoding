from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd

df_mentor = pd.read_csv("C:/Users/Asus/pyton for data science/df_mentor_fix1 (1).csv")

class Mentee:
    def __init__(self, name, needs):
        self.name = name
        self.needs = needs

class Mentor:
    def __init__(self, name, expertise, rating):
        self.name = name
        self.expertise = expertise
        self.rating = rating

class MentoringPlatform:
    def __init__(self):
        self.mentees = []
        self.mentors = []
        self.vectorizer = TfidfVectorizer()

    def add_mentee(self, mentee):
        self.mentees.append(mentee)

    def add_mentor(self, mentor):
        self.mentors.append(mentor)

    def preprocess_text(self, text):
        stop_words = set(stopwords.words('english') + stopwords.words('indonesian'))
        tokens = word_tokenize(text.lower())
        filtered_tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
        preprocessed_text = ' '.join(filtered_tokens)
        return preprocessed_text

    def fit_vectorizer(self):
        corpus = []
        for mentee in self.mentees:
            corpus.append(self.preprocess_text(mentee.needs))
        for mentor in self.mentors:
            corpus.append(self.preprocess_text(mentor.expertise))
        self.vectorizer.fit(corpus)

    def find_mentor(self, mentee_name, mentee_needs):
        mentee_needs = self.preprocess_text(mentee_needs)
        mentee_vector = self.vectorizer.transform([mentee_needs])

        matched_mentors = []
        for mentor in self.mentors:
            mentor_expertise = self.preprocess_text(mentor.expertise)
            mentor_vector = self.vectorizer.transform([mentor_expertise])

            similarity_score = cosine_similarity(mentee_vector, mentor_vector)[0][0]
            if similarity_score > 0:
                matched_mentors.append((mentor, similarity_score))
        matched_mentors = sorted(matched_mentors, key=lambda x: (x[1] + x[0].rating), reverse=True)

        return matched_mentors

    def match_mentee_with_mentor(self, mentee_name, mentee_needs):
        matched_mentors = self.find_mentor(mentee_name, mentee_needs)
        if len(matched_mentors) > 0:
            print(f"Mentee '{mentee_name}' cocok dengan mentor:")
            for mentor, similarity_score in matched_mentors:
                print(f" - Name   : {mentor.name}")
                print(f" - Expertise : {mentor.expertise}")
                print(f" - Rating : {mentor.rating}")
                print()
        else:
            print(f"Mentee '{mentee_name}' tidak ditemukan mentor yang cocok.")

platform = MentoringPlatform()

for _, row in df_mentor.iterrows():
    platform.add_mentee(Mentee(row['name'], row['need']))

# Add mentors using platform.add_mentor() method

platform.fit_vectorizer()

name = 'mentees 1'
need = 'mau cari mentees yang paham Machine Learning'
platform.match_mentee_with_mentor(name, need)
