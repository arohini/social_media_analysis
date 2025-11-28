from flask import Flask, jsonify, url_for, request
from .storage_connection import *
import json
import pandas as pd
import logging

app = Flask(__name__)
# Basic configuration for console output
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# You can also add file handlers for persistent logs
file_handler = logging.FileHandler('sm_analysis_app.log')
file_handler.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

mdo = MongodbOperations("social_media_analysis")

sm_data = pd.read_csv('data/smmh.csv')


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

@app.route('/add-sm-data', methods=['POST'])
def add_item():
    try:
        data = request.json # Assuming data is sent as JSON
        collection = "raw_data"
        mdo.insert_one(collection,data) # Using PyMongo directly
        return jsonify({"message": "Item added successfully"}), 200
    except Exception as e:
        print(f"Error adding data to mongo collection", str(e))

@app.route('/get-sm-user/<int:user_id>', methods=['GET'])
def get_sm_user(user_id):
    try:
        collection = "raw_data"
        sm_user_data = mdo.find(collection,{'user_id': user_id}) # Using PyMongo directly
        if sm_user_data:
            for doc in sm_user_data:
                del doc['_id']
                return jsonify(doc)
        else:
            return f"User id: {user_id} document not found !"
    except Exception as e:
        print(f"Error retrieving sm user data", str(e))
        return jsonify({'error': 'Error retrieving sm user data'}), 400


@app.route('/update-sm-data/<user_id>', methods=['PUT'])
def update_item(user_id):
    try:
        collection = "raw_data"
        data = json.dumps(request.json)
        mdo.update_one(collection, {"user_id": user_id}, {"$set": data})
        return jsonify({"message": "updated the data successfully"}), 200
    except Exception as e:
        print("Error putting the data to mongo document", str(e))
        return jsonify({"error": "Error putting the data to mongo document"}), 400

@app.route('/delete-sm-user/<user_id>', methods=['DELETE'])
def delete_item(user_id):
    try:
        collection = "raw_data"
        deleted_doc = mdo.delete_one(collection, {"user_id": user_id})
        print("="*1000)
        print(f"{deleted_doc.deleted_count} document(s) deleted.")
        return jsonify({"message": "Item deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Error deleting the document for user id: {user_id}"}), 400

if __name__ == '__main__':
    app.run(debug=True)