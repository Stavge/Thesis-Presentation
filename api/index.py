from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/scenario/<num>')
def get_scenario(num):
    return jsonify({"test": "data"})  # Προσωρινό
