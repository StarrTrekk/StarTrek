from openai import OpenAI
import time
import logging
from datetime import datetime

client = OpenAI(
   api_key="sk-proj-6c1pIe8N10Hwt87G6eW7T3BlbkFJlyHBdEYskBnEKw3qXaYL"
   )

# === Hardcode our ids ===
assistant_id = "asst_kgzXAaSmgKldHgrL3YTQ2EVE"
thread_id = "thread_7A32BY0HnfYmSmHy7631bKR0"


def all_tache(message, thread_id = thread_id, assistant_id = assistant_id):
    message = client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=message
    )
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run.completed_at:
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistant Response: {response}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(5)
    return response





all_tache("qu'est ce que je peux faire prêt de paris ?")

# === Run ===
