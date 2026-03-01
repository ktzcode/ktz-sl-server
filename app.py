from flask import Flask, jsonify
import requests
import re

app = Flask(__name__)

@app.route('/profile/<uuid>', methods=['GET'])
def get_profile_picture(uuid):
    try:
        # Consultar el perfil de SL
        url = f"https://api.secondlife.com/avatar/{uuid}/complete"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return jsonify({"texture": "5748decc-f629-461c-9a36-a35a221fe21f", "error": "avatar_not_found"})
        
        data = response.json()
        
        # Extraer UUID de la foto de perfil
        texture_uuid = None
        
        if 'image_id' in data:
            texture_uuid = data['image_id']
        elif 'profile' in data and 'image_id' in data['profile']:
            texture_uuid = data['profile']['image_id']
        
        if not texture_uuid or texture_uuid == "00000000-0000-0000-0000-000000000000":
            return jsonify({"texture": "5748decc-f629-461c-9a36-a35a221fe21f", "status": "no_photo"})
        
        return jsonify({"texture": texture_uuid, "status": "ok"})
    
    except Exception as e:
        return jsonify({"texture": "5748decc-f629-461c-9a36-a35a221fe21f", "error": str(e)})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "alive"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
