from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

PATH_KEY = ".secret.key"
HOST = os.getenv("HOST", "localhost")

app = Flask(__name__)
CORS(app)

# Configure OpenAI API Key
client = OpenAI(api_key='sk-proj-6c1pIe8N10Hwt87G6eW7T3BlbkFJlyHBdEYskBnEKw3qXaYL')

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es Star-trek un expert de trek, ton role est de répondre aux questions des utilisateurs sur les treks en france. Tu peux aussi donner des conseils sur les treks à faire en france. Mais toujours répondre d'une façon très sobre"},
                {"role": "user", "content": user_message}
            ]
        )
        #transform the response to a json object
        return jsonify({'reply': completion.choices[0].message.content})

    except Exception as e:
        return jsonify({'error'}) 
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
