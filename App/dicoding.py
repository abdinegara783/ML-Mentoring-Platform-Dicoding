from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mentoring"]
mentees = mydb["mentees"]
mentorsCol = mydb["mentors"]
reviews = mydb["reviews"]

df_mentor = pd.read_csv(
    "/Users/cisnux/ApplicationDevelopments/ML-Mentoring-Platform-Dicoding/App/df_mentor_fix1 (1).csv"
)
df_mentor["TF_IDF"] = df_mentor[["about", "Learning_path", "skills"]].apply(
    lambda x: ", ".join(x.dropna().astype(str)), axis=1
)


class Mentee:
    def __init__(self, name, needs):
        self.name = name
        self.needs = needs


class GetMentor:
    def __init__(self, id, fullName, profilePicture, job, rating):
        self.id = id
        self.fullName = fullName
        self.profilePicture = profilePicture
        self.job = job
        self.rating = rating

    def __dict__(self):
        return {
            "id": self.id,
            "fullName": self.fullName,
            "photoProfile": self.profilePicture,
            "job": self.job,
            "rating": self.rating,
        }


class Mentor:
    def __init__(self, mentor_id, name, expertise, rating, jobs, pictures):
        self.mentor_id = mentor_id
        self.name = name
        self.expertise = expertise
        self.rating = rating
        self.jobs = jobs
        self.pictures = pictures

    def __dict__(self):
        return {
            "id": self.mentor_id,
            "fullName": self.name,
            "expertises": self.expertise,
            "rating": self.rating,
            "job": self.jobs,
            "photoProfile": self.pictures,
        }


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
        stop_words = set(stopwords.words("english") + stopwords.words("indonesian"))
        tokens = word_tokenize(text.lower())
        filtered_tokens = [
            token for token in tokens if token.isalpha() and token not in stop_words
        ]
        preprocessed_text = " ".join(filtered_tokens)
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
        matched_mentors = sorted(
            matched_mentors, key=lambda x: (x[1] + x[0].rating), reverse=True
        )

        return matched_mentors

    def match_mentee_with_mentor(self, mentee_name, mentee_needs):
        matched_mentors = self.find_mentor(mentee_name, mentee_needs)
        mentors = []
        if len(matched_mentors) > 0:
            print(f"Kamu cocok dengan mentor:")
            for mentor, similarity_score in matched_mentors:
                print(f"ID       : {mentor.mentor_id}")
                print(f"Name     : {mentor.name}")
                print(f"Rating   : {mentor.rating}")
                print(f"Jobs     : {mentor.jobs}")
                print(f"Pictures : {mentor.pictures}")
                print()
                mentors.append(
                    GetMentor(
                        mentor.mentor_id,
                        mentor.name,
                        mentor.pictures,
                        mentor.jobs,
                        mentor.rating,
                    )
                )

        else:
            print(f"tidak ditemukan mentor yang cocok.")
        return mentors


def setMentorsInput(userId):
    platform = MentoringPlatform()
    mentors = []
    mentorsInput = mentorsCol.find({"id": {"$ne": userId}})
    for mentor in mentorsInput:
        reviewResult = list(
            reviews.aggregate(
                [
                    {
                        "$group": {
                            "_id": "$mentorId",
                            "totalRating": {"$sum": "$rating"},
                            "count": {"$sum": 1},
                        }
                    },
                    {
                        "$project": {
                            "_id": 0,
                            "mentorId": "$_id",
                            "averageRating": {"$divide": ["$totalRating", "$count"]},
                        }
                    },
                    {"$match": {"mentorId": mentor["id"]}},
                ]
            )
        )
        mentorProfile = mentees.find_one(
            {"id": mentor["id"]},
            {"_id": 0, "id": 1, "fullName": 1, "photoProfile": 1, "job": 1},
        )
        skills = []
        for expertise in mentor["expertises"]:
            for skill in expertise["skills"]:
                skills.append(skill)

        stringSkills = " ".join(skills)
        if len(reviewResult) == 0:
            platform.add_mentor(
                Mentor(
                    mentor["id"],
                    mentorProfile["fullName"],
                    stringSkills,
                    0.0,
                    mentorProfile["job"],
                    mentorProfile["photoProfile"],
                )
            )
        else:
            platform.add_mentor(
                Mentor(
                    mentor["id"],
                    mentorProfile["fullName"],
                    stringSkills,
                    float(reviewResult[0]),
                    mentorProfile["job"],
                    mentorProfile["photoProfile"],
                )
            )
    platform.fit_vectorizer()
    return platform


platform = MentoringPlatform()


for index, row in df_mentor.iterrows():
    mentor_expertise = " ".join(row["TF_IDF"].split(","))
    mentor = Mentor(
        row["ID"],
        row["name"],
        mentor_expertise,
        row["rating"],
        row["Jobs"],
        row["Pictures"],
    )
    platform.add_mentor(mentor)

# Fitting vectorizer
platform.fit_vectorizer()
