from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/hello-world', methods=['GET'])
def hello_world():
    return jsonify({
        "status": "success",
        "message": "Merhaba Dünya! Flask API çalışıyor."
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)