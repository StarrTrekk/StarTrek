

#Build a application with open ai api 

from openai import OpenAI

client = OpenAI(
   api_key="sk-proj-6c1pIe8N10Hwt87G6eW7T3BlbkFJlyHBdEYskBnEKw3qXaYL"
   )


audio = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input= "Casanova el tranfinquinté le hagard",
        )

#we have now a audio file that we can play
audio.stream_to_file("output.mp3")




