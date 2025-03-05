import json

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)

CORS(app, resources={r"/webhook": {"Access-Control-Allow-Origin": "https://na.mabibase.com/",
                                   "methods": ["GET", "POST", 'OPTIONS'],
                                   "allowed_headers": ['Authorization', "Content-Type",
                                                       "Access-Control-Allow-Origin"]}})


@app.route('/webhook', methods=['GET', 'POST', 'OPTIONS'])
def webhook_handler():
    headers = {
        "Content-Type": "application/json"
    }
    target_webhook = 'https://discord.com/api/webhooks/1346352200867250259/LDy0ADoORrAfSPNPn_HsFCkHVryUwPeeenCdpM12MxljjWURY8Yzjc-5IxfuzjYibGac'
    if request.method == 'POST':
        data = request.get_json()
        print('Data received from webhook:', data)
        data['username'] = 'Forward From MabiBase'
        data['content'] = "Test Forward From MabiBase: "
        if 'embeds' in data:
            data['content'] += data['embeds'][0]['fields'][2]['value']

        # post to discord
        resp = requests.post(target_webhook, data=json.dumps(data), headers=headers)
        if resp.status_code == 200:
            return jsonify({'status': 'success'}), 200
        return jsonify({'status': 'success'}), 200

    elif request.method == 'OPTIONS':
        return '', 200, {'Allow': 'GET, POST, OPTIONS'}
    else:
        return 'Method not allowed', 405


if __name__ == '__main__':
    app.run(debug=True)
