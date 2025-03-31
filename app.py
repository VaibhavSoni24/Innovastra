from flask import Flask, request, jsonify, render_template
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)
BOT_ID = "56675127"
BASE_URL = "https://www.botlibre.com/rest/api/form-chat"

def chat_with_bot(message):
    params = {
        "instance": BOT_ID,
        "message": message,
        "application": "2634971016006089022"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        xml_response = response.text
        root = ET.fromstring(xml_response)
        bot_message = root.find("message").text
        return bot_message
    else:
        return f"Error {response.status_code}: {response.text}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/practice')
def practice():
    return render_template('practice.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"reply": "I didn't receive any message. Please try again!"})
    bot_reply = chat_with_bot(user_message)
    return jsonify({"reply": bot_reply})
if __name__ == '__main__':
    app.run(debug=True)