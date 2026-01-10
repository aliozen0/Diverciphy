from flask import Flask, request, jsonify
import os
app = Flask(__name__) #TODO: Create global architecture for app object.

@app.route('/recieve_public_key', methods=['POST'])
def recieve_public_key():
    data = request.get_json(silent=True)

    print(f"Public Key Recieved: {data['public_key']}")

    if not data:
        return jsonify({"hata": "JSON gövdesi boş veya hatalı!"}), 400
    write_public_key_to_file(data['public_key'], '../../keys/recieved_keys/recieved_key.pem')
    return jsonify({"durum": "basarili"}), 200

def write_public_key_to_file(public_key_pem: str, file_path: str):
    try:
        with open(file_path, 'wb') as f:
            f.write(public_key_pem.encode('utf-8'))
        print(f"Public key successfully written to {file_path}")
    
    except FileNotFoundError:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(public_key_pem.encode('utf-8'))
        print(f"Directory created and public key written to {file_path}")

    except Exception as e:
        print(f"Error writing public key to file: {e}")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
        