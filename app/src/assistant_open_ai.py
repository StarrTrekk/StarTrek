


from openai import OpenAI
import time
#we gonna work with the openai api assistant

client = OpenAI(
   api_key="sk-proj-6c1pIe8N10Hwt87G6eW7T3BlbkFJlyHBdEYskBnEKw3qXaYL"
   )


#we gonna create a thread with a assistant openai osbject
import os
from openai import OpenAI, AsyncOpenAI
import asyncio
import time

# env variables

my_key = "sk-proj-6c1pIe8N10Hwt87G6eW7T3BlbkFJlyHBdEYskBnEKw3qXaYL"

# OpenAI API
client = AsyncOpenAI(api_key=my_key)
assistant_id = "asst_kgzXAaSmgKldHgrL3YTQ2EVE"


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


if __name__ == "__main__":
    async def main():
    
        # Create assistant and thread before entering the loop
        #thread = await client.beta.threads.create()
        thread_id = "thread_7A32BY0HnfYmSmHy7631bKR0"
        while True:
            question = input("How may I help you today? \n")
            if "exit" in question.lower():
                break
            
            # Add message to thread
            await add_message_to_thread(thread_id, question)
            message_content = await get_answer(assistant_id , thread_id=thread_id)
            print(message_content)
    asyncio.run(main())