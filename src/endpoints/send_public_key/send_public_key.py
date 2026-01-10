from flask import Flask, request, jsonify
from src.core.assemble import Assemble
from dotenv import load_dotenv
import os
app = Flask(__name__) #TODO: Create global architecture for app object.

def read_public_key_from_file(file_path: str):
    try:
        load_dotenv()
        assembler = Assemble(components=[])
        assembler.generate_and_save_keys(password=os.environ.get("FILE_PASSWORD"), file_path=file_path)
        
        with open(file_path, 'rb') as f:
            return f.read().decode('utf-8')

    except Exception as e:
        print(f"Error reading public key from file: {e}")
        return None

import requests
from flask import Flask, request, jsonify

@app.route('/send_public_key', methods=['GET', 'POST'])
def send_public_key():
    public_key = read_public_key_from_file('../../keys/generated_keys/generated_public.pem')
    
    if not public_key:
        return jsonify({"error": "Public key could not be read!"}), 500

    if request.method == 'GET':
        return jsonify({"public_key": public_key}), 200

    if request.method == 'POST':
        data = request.get_json()
        
        target_address = data.get('address')
        if not target_address:
            return jsonify({"error": "Missing 'address' key in JSON body!"}), 400

        try:
            response = requests.post(target_address, json={"public_key": public_key}, timeout=5)
            
            return jsonify({
                "status": "success",
                "target_address": target_address,
                "remote_response": response.json()
            }), response.status_code

        except requests.exceptions.RequestException as e:
            return jsonify({"error": f"Failed to send request: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
        