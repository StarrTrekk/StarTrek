from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from geopy.geocoders import Nominatim
from openai import OpenAI, AsyncOpenAI
import os
from werkzeug.utils import secure_filename
from io import BytesIO
import asyncio
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locations.db'
db = SQLAlchemy(app)
geolocator = Nominatim(user_agent="StarTrek")
# Configure OpenAI API Key
client = OpenAI(api_key='sk-proj-6c1pIe8N10Hwt87G6eW7T3BlbkFJlyHBdEYskBnEKw3qXaYL')


my_key = "sk-proj-6c1pIe8N10Hwt87G6eW7T3BlbkFJlyHBdEYskBnEKw3qXaYL"

# OpenAI API
client_ass = AsyncOpenAI(api_key=my_key)
assistant_id = "asst_kgzXAaSmgKldHgrL3YTQ2EVE"
thread_id = "thread_7A32BY0HnfYmSmHy7631bKR0"

app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


async def add_message_to_thread(thread_id, user_question):
    # Create a message inside the thread
    message = await client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content= user_question
    )
    return message


async def get_answer(assistant_id, thread_id):
    print("Thinking...")
    # run assistant
    print("Running assistant...")
    run =  await client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    # wait for the run to complete
    while True:
        runInfo = await client.beta.threads.runs.retrieve(thread_id = thread_id, run_id=run.id)
        if runInfo.completed_at:
            print(f"Run completed")
            break
        print("Waiting...")
        time.sleep(1)

    print("All done...")
    # Get messages from the thread
    messages = await client.beta.threads.messages.list(thread_id)
    message_content = messages.data[0].content[0].text.value
    return message_content


async def hab(question):
        # Add message to thread
        await add_message_to_thread(thread_id, question)
        message_content = await get_answer(assistant_id , thread_id=thread_id)
        #print(message_content)
        return message_content

def audio_to_text(audio_file):
    audio_file= open(audio_file, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    return transcription.text

def text_to_audio(text):
    audio = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input= text, 
        )

    #we have now a audio file that we can play
    audio.stream_to_file("reponse.wav")

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Location {self.id} ({self.latitude}, {self.longitude})>'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/locate', methods=['POST'])
def locate():
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    location = Location(latitude=latitude, longitude=longitude)
    db.session.add(location)
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/follow')
def follow():
    locations = Location.query.order_by(Location.id.desc()).limit(10).all()
    return jsonify([{'latitude': location.latitude, 'longitude': location.longitude} for location in locations])

"""
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
        return jsonify({'error': str(e)}), 500

"""

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()  # No await here
    question = data.get('message')
    if question:
        # execute python script with os.system
        os.system(f'python3 chat.py "{question}"')
        # get the response from the file
        with open("response.txt", "r") as file:
            reponse = file.read()
        return jsonify({'reply': reponse})
    return jsonify({'error': 'No message received'})

@app.route('/vocal', methods=['POST'])
def vocal():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Convert audio to text
        text = audio_to_text(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Get response from OpenAI
        try:
            """
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Tu es Star-trek un expert de trek, ton role est de répondre aux questions des utilisateurs sur les treks en france. Tu peux aussi donner des conseils sur les treks à faire en france. Mais toujours répondre d'une façon très sobre"},
                    {"role": "user", "content": text}
                ]
            )
            """
            os.system(f'python3 chat.py "{text}"')
            # Get the response from the file
            with open("response.txt", "r") as file:
                reponse = file.read()

            # Convert text to audio
            text_to_audio(reponse)

            # send the audio file and the response
            return send_file("reponse.wav", as_attachment=True), jsonify({'reply': reponse})

        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    return jsonify({'error': 'File upload failed'})

if __name__ == '__main__':
    #db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True,use_reloader=False)
