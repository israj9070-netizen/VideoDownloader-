from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Cobalt API Configuration (Free & Powerful)
COBALT_API_URL = "https://api.cobalt.tools/api/json"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_video_info', methods=['POST'])
def get_video_info():
    data = request.get_json()
    video_url = data.get('url')

    if not video_url:
        return jsonify({"status": "error", "message": "Link kahan hai bhai?"})

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Cobalt API Body
    payload = {
        "url": video_url,
        "vQuality": "720", # High quality
        "isAudioOnly": False,
        "filenamePattern": "basic"
    }

    try:
        # Requesting Cobalt API
        response = requests.post(COBALT_API_URL, json=payload, headers=headers, timeout=15)
        res_data = response.json()

        if res_data.get('status') == 'picker':
            # Agar multiple qualities milein toh pehli wali utha lo
            video_data = res_data['picker'][0]
            return jsonify({
                "status": "success",
                "title": "Video Found (Multiple Qualities)",
                "thumbnail": "https://img.freepik.com/free-vector/play-button-icon-vector-illustration-isolated_24911-45184.jpg", # Placeholder
                "download_url": video_data['url']
            })

        if res_data.get('status') == 'stream' or res_data.get('status') == 'redirect':
            # Success! Video link mil gaya
            return jsonify({
                "status": "success",
                "title": "Aapki Video Taiyar Hai! 🔥",
                "thumbnail": "https://img.freepik.com/free-vector/video-player-interface-design_1017-15206.jpg", # Placeholder
                "download_url": res_data['url']
            })
        
        else:
            return jsonify({"status": "error", "message": "API ne mana kar diya. Link check karo."})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": "Server busy hai, thodi der baad try karein."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

