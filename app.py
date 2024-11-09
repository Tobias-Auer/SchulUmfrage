from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import Logger
import db_connect
app = Flask(__name__)
CORS(app)

logger = Logger.logger("dbManager")
db = db_connect.dbManager(logger)

def validate_auth(auth):
    try:
        id, checksum = auth.split(":")
    except ValueError:
        return False
    logger.info("validating auth")
    logger.info(f"checksum: {type(checksum)}\nhashed: {type(reverse_obfuscated_algorithm(id))}")
    return str(checksum) == str(reverse_obfuscated_algorithm(id))

def process_geo_id(auth_id, geo_id):
    db.modify_entry(auth_id, geo_id)
    return "done"

@app.route('/', methods=['POST'])
def index():
    data = request.json

    if 'auth' not in data or 'geoID' not in data:
        return jsonify({'message': 'Missing parameters'}), 400

    auth = data['auth']
    geo_id = data['geoID']

    if validate_auth(auth):
        result = process_geo_id(auth, geo_id)
        return jsonify({'message': result}), 200
    else:
        return jsonify({'message': 'Invalid auth'}), 403

@app.route('/view')
def view():
    return db.view_all()

@app.route("/data")
def get_data():
    count = request.args.get('count', default=999, type=int)
    data = db.view_all(count)
    votes = db.getStudentCount(count)
    votesTotal = db.getTotalVotes(count)
    maxStudentCount = db.getMostFrequentStudentCount(count)
    ignoredVotes = db.getIgnoredStudents(count)
    return render_template('blank_map.html', data=data, placeList=data[0:10], votes=votes, votesTotal=votesTotal, maxCount=maxStudentCount, currentMaxCount=count, ignoredVotes=ignoredVotes)

@app.route('/get', methods=['GET'])
def getUserVotes():
    user_id = request.args.get('userID')

    if user_id is None: 
        return jsonify({'message': 'Missing parameters'}), 400

    auth = user_id
    if validate_auth(auth):
        result = db.get_entries_by_user_id(auth)
        return jsonify({'message': result}), 200
    else:
        return jsonify({'message': 'Invalid auth'}), 403

@app.route('/admin', methods=['GET'])
def admin():
    return jsonify({'message': 'Welcome to the admin page!'}), 200

def reverse_obfuscated_algorithm(input_string):
    input_string = str(input_string)
    hash_value = 0

    if len(input_string) == 0:
        return hash_value  # Returns 0 for empty strings

    for char in input_string:
        char_code = ord(char)  # Get the Unicode code point of the character
        hash_value = ((hash_value << 5) - hash_value) + char_code
        # Simulate 32-bit signed integer overflow
        hash_value = hash_value & 0xFFFFFFFF  # Keep it within 32 bits

    # Convert to signed 32-bit integer
    if hash_value >= 0x80000000:
        hash_value -= 0x100000000  # Convert to negative if needed

    logger.info(hash_value)
    return hash_value  # Return the final hash value


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
