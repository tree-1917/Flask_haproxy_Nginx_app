from flask import Flask, jsonify, send_from_directory

app = Flask(__name__)

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/api/v1', methods=['GET'])
def api_v1():
    return jsonify({
        'status': 'success',
        'message': 'Welcome to API v1 @ 5001',
        'data': {
            'version': '1.0',
            'features': ['feature1', 'feature2']
        }
    })

if __name__ == '__main__':
    print("This is Main File")
    # app.run(host='0.0.0.0', port=5001)
