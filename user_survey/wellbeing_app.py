from flask import Flask, jsonify, url_for, request
import json
import pandas as pd

app = Flask(__name__)

sm_data = pd.read_csv('data/smmh.csv')

@app.route("/about-me", methods=["GET"])
def about_me():
    about_me_data = {"name": "rohini", "skills": ["python", "sql"]}
    return jsonify(about_me_data), 200

@app.route("/sm-user-survey", methods=["GET"])
def user_survey_response():
    sm_cols = get_survey_data()
    print(sm_cols)
    data = {'cols': sm_cols}
    return jsonify(data) , 200


@app.route("/sm-platform-info", methods=["GET"])
def get_social_media_platform_info():
    sm_data_info = {}
    sm_data.rename(columns={'7. What social media platforms do you commonly use?': 
                            'sm_platforms'}, inplace=True)
    sm_platforms = list(sm_data['sm_platforms'])
    sm_data_count = len(sm_data)
    sm_data_info['total_survey_count'] = sm_data_count
    sm_data_info['social_media_platforms'] = sm_platforms
    return jsonify(sm_data_info), 200

@app.route('/sm-filter', methods=['POST'])
def get_sm_filtered_data():
    try:
        data = request.get_json()
        from_age = data['from_age']
        to_age = data['to_age']
        age = sm_data[(sm_data['1. What is your age?'] > from_age) &
                      (sm_data['1. What is your age?'] < to_age)]
        sm_data_count = len(age)
        sum_of_age = age['1. What is your age?'].sum()
        
        average = sum_of_age / sm_data_count
        result = {'sum_of_age': sum_of_age, 'average': average}
        return jsonify({'result': result})
    except ZeroDivisionError:
        return jsonify({'error': 'Cannot divide by zero'}), 400
    except KeyError:
        return jsonify({'error': 'Missing numerator or denominator in request body'}), 400
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

@app.route('/sm-/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates an existing user."""
    update_data = request.get_json()
    if not update_data:
        return jsonify({"error": "No data provided for update"}), 400

    for user in users:
        if user['id'] == user_id:
            if 'name' in update_data:
                user['name'] = update_data['name']
            if 'email' in update_data:
                user['email'] = update_data['email']
            return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/sm-filter/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a user."""
    global users
    initial_length = len(users)
    users = [user for user in users if user['id'] != user_id]
    if len(users) < initial_length:
        return jsonify({"message": f"User {user_id} deleted"}), 200
    return jsonify({"error": "User not found"}), 404

# user_profile_url = url_for('show_user_profile', username='rohini')

if __name__ == '__main__':
    app.run(debug=True)