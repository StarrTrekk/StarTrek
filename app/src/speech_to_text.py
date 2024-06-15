

#Build a application with open ai api 

from openai import OpenAI

client = OpenAI(
   api_key="sk-proj-6c1pIe8N10Hwt87G6eW7T3BlbkFJlyHBdEYskBnEKw3qXaYL"
   )



audio_file= open("output.mp3", "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)
print(transcription.text)




