from flask import Flask, jsonify, request
from dicoding import platform

app = Flask(__name__)

@app.route('/matchmaking', methods=['POST'])
def matchmaking():
    data = request.get_json()
    Learning_path = data['Learning_path']
    need = data['need']
    
    mentors = platform.match_mentee_with_mentor(Learning_path, need)
    
    if len(mentors) > 0:
        mentor_list = [{
            "id": mentor.mentor_id,
            "photoProfile": mentor.pictures,
            "fullName": mentor.name,
            "job": mentor.jobs,
            "averageRating": mentor.rating
        } for mentor, _ in mentors]
        
        response = {
            "status": "success",
            "data": {
                "mentors": mentor_list
            }
        }
    else:
        response = {
            "status": "success",
            "data": {
                "mentors": []
            }
        }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run()
