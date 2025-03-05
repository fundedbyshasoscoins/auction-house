import json

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from api_call import get_item_results

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
    target_webhook = 'https://discord.com/api/webhooks/1346769346785054740/7YVRPYPonzbdqenFAgFpYYU8_wVg6U3lR1l5W2BQ7TQOapZPRxY0Hr_dIHVGlncLqr--'
    if request.method == 'POST':
        data = request.get_json()
        print('Data received from webhook:', data)
        # data['username'] = 'Forward From MabiBase'
        # data['content'] = "Test Forward From MabiBase: "
        # if 'embeds' in data:
        #     data['content'] += data['embeds'][0]['fields'][2]['value']
        resp1 = requests.post(target_webhook, data=json.dumps(data), headers=headers)
        if 'embeds' in data:
            data_url = data['embeds'][0]['fields'][2]['value']
            price_result = get_item_results(data_url)
            content = f"```{json.dumps(price_result, indent=4)}```"
            priceData = {
                'username': "auction_house_spy",
                'content': content,
            }

            # post to discord
            resp2 = requests.post(target_webhook, data=json.dumps(priceData), headers=headers)
            if resp1.status_code == 200 and resp2.status_code == 200:
                return jsonify({'status': 'success'}), 200

        return jsonify({'status': 'success'}), 200

    elif request.method == 'OPTIONS':
        return '', 200, {'Allow': 'GET, POST, OPTIONS'}
    else:
        return 'Method not allowed', 405


if __name__ == '__main__':
    app.run(debug=True)
