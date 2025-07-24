from flask import Flask, jsonify
import numpy as np

app = Flask(__name__)
a = np.arange(10)

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        "message": "Hello, World!",
        "status": "success"
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)