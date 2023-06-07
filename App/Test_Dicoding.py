from flask import Flask, request
from dicoding import platform

app = Flask(__name__)

@app.route('/mentors', methods=['GET'])
def get_matched_mentors():
    learning_path = request.args.get('learning_path')
    need = request.args.get('need')
    matched_mentors = platform.find_mentor(learning_path, need)

    if len(matched_mentors) > 0:
        response = "<h2>Kamu cocok dengan mentor:</h2>"
        for mentor, similarity_score in matched_mentors:
            response += f"<p>ID: {mentor.mentor_id}</p>"
            response += f"<p>Name: {mentor.name}</p>"
            response += f"<p>Rating: {mentor.rating}</p>"
            response += f"<p>Jobs: {mentor.jobs}</p>"
            response += "<br>"
    else:
        response = "<h2>Tidak ditemukan mentor yang cocok.</h2>"

    return response

if __name__ == '__main__':
    app.run()

