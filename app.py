from flask import Flask, request, jsonify, abort
import uuid  # For unique IDs

app = Flask(__name__)

# In-memory storage (list of dicts)
notes = []

@app.route('/notes', methods=['GET'])
def get_notes():
    return jsonify({'notes': notes})

@app.route('/notes', methods=['POST'])
def create_note():
    if not request.json or 'title' not in request.json:
        abort(400, description="Missing the 'title' in JSON")
    
    new_note = {
        'id': str(uuid.uuid4()),  # Unique ID
        'title': request.json['title'],
        'content': request.json.get('content', ''),
        'created_at': request.json.get('created_at', 'now')
    }
    notes.append(new_note)
    return jsonify({'note': new_note}), 201

@app.route('/notes/<note_id>', methods=['GET'])
def get_note(note_id):
    note = next((n for n in notes if n['id'] == note_id), None)
    if note is None:
        abort(404, description="Note not found")
    return jsonify({'note': note})

@app.route('/notes/<note_id>', methods=['PUT'])
def update_note(note_id):
    note = next((n for n in notes if n['id'] == note_id), None)
    if note is None:
        abort(404, description="Note not found")
    
    if not request.json:
        abort(400, description="No JSON data provided")
    
    note['title'] = request.json.get('title', note['title'])
    note['content'] = request.json.get('content', note['content'])
    note['updated_at'] = request.json.get('updated_at', 'now')
    return jsonify({'note': note})

@app.route('/notes/<note_id>', methods=['DELETE'])
def delete_note(note_id):
    global notes
    note = next((n for n in notes if n['id'] == note_id), None)
    if note is None:
        abort(404, description="Note not found")
    
    notes = [n for n in notes if n['id'] != note_id]
    return jsonify({'message': 'Note deleted'})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': str(error)}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': str(error)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)