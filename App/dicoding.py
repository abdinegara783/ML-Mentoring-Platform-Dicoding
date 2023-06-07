from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd

df_mentor = pd.read_csv("C:/Users/Asus/pyton for data science/df_mentor_fix1 (1).csv")
df_mentor['TF_IDF'] = df_mentor[['about', 'Learning_path', 'skills']].apply(lambda x: ', '.join(x.dropna().astype(str)), axis=1)
class Mentee:
    def __init__(self, name, needs):
        self.name = name
        self.needs = needs

class Mentor:
    def __init__(self, mentor_id, name, expertise, rating, jobs, pictures):
        self.mentor_id = mentor_id
        self.name = name
        self.expertise = expertise
        self.rating = rating
        self.jobs = jobs
        self.pictures = pictures


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
            print(f"Kamu cocok dengan mentor:")
            for mentor, similarity_score in matched_mentors:
                print(f"ID       : {mentor.mentor_id}")
                print(f"Name     : {mentor.name}")
                print(f"Rating   : {mentor.rating}")
                print(f"Jobs     : {mentor.jobs}")
                print(f"Pictures : {mentor.pictures}")
                print()
        else:
            print(f"tidak ditemukan mentor yang cocok.")
name=["Android", "Front-End", "Back-End", "iOS", "Cloud", "Machine Learning", "UI/UX", "Game", "web", "analys"]
platform = MentoringPlatform()


for index, row in df_mentor.iterrows():
    mentor_expertise = ' '.join(row['TF_IDF'].split(","))
    mentor = Mentor(row['ID'], row['name'], mentor_expertise, row['rating'], row['Jobs'], row['Pictures'])
    platform.add_mentor(mentor)

# Fitting vectorizer
platform.fit_vectorizer()