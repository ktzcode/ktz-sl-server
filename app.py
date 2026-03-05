from flask import Flask, jsonify
import requests
import os # Importar os para leer variables de entorno

app = Flask(__name__)

@app.route('/profile/<uuid>', methods=['GET'])
def get_profile_picture(uuid):
    print(f"--- Petición recibida para UUID: {uuid} ---") # Debug en logs de Render
    
    try:
        # Consultar el perfil de SL
        # Nota: Esta API de SL a veces es lenta o requiere headers específicos
        url = f"https://api.secondlife.com/avatar/{uuid}/complete"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        print(f"Consultando API SL: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        
        print(f"Status SL API: {response.status_code}")
        
        if response.status_code != 200:
            print("Error: Avatar no encontrado en SL API")
            return jsonify({"texture": "5748decc-f629-461c-9a36-a35a221fe21f", "error": "avatar_not_found"})
        
        data = response.json()
        
        # Extraer UUID de la foto de perfil
        texture_uuid = None
        
        # Intentar encontrar el ID en la raíz o dentro de 'profile'
        if 'image_id' in data:
            texture_uuid = data['image_id']
        elif 'profile' in data and 'image_id' in data['profile']:
            texture_uuid = data['profile']['image_id']
            
        print(f"Texture UUID extraido: {texture_uuid}")
        
        if not texture_uuid or texture_uuid == "00000000-0000-0000-0000-000000000000":
            print("Error: Avatar no tiene foto")
            return jsonify({"texture": "5748decc-f629-461c-9a36-a35a221fe21f", "status": "no_photo"})
        
        print(f"EXITO: Retornando JSON con textura {texture_uuid}")
        return jsonify({"texture": texture_uuid, "status": "ok"})
    
    except Exception as e:
        print(f"ERROR INTERNO: {str(e)}")
        return jsonify({"texture": "5748decc-f629-461c-9a36-a35a221fe21f", "error": str(e)})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "alive"})

if __name__ == '__main__':
    # CORRECCIÓN RENDER: Leer el puerto de la variable de entorno
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
