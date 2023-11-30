#!/usr/bin/env python3
## TCP AI Chat Room 
## (c) 2021-2023  Kerry Fraser-Robinson

import socket
import threading
import openai
import os
import tiktoken 

ai_chat_name = 'ai_George'
ai_type = 'and helpful'
ai_specialty = 'comedy'
ai_reputation = 'witty banter'
ai_goal = 'entertain'

system_message = f'Your name is {ai_chat_name}. You are an experienced {ai_type} assistant, specialized in {ai_specialty} with a reputation for {ai_reputation}. Your goal is to {ai_goal}. Please refrain from starting your responses with your chat tag, {ai_chat_name}. Consider your response carefully and if it is superfluous, unnecessary, neither adds new information nor contributes to the flow of the conversation, simply respond with "<listens>" (without quotation marks). Otherwise, please keep your responses brief unless specifically asked to be more verbose. If the most recent message in this conversation is specifically directed or addressed to user other than {ai_chat_name}, please simply respond with "<looks at username>" where username has been replaced with the name of the user that you would expect to respond.'

#### Note: needs a Conversation Master to observe conversation and pass it to the most appropriate respondant

# system_message = 'You are a helpful assistant.'

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

def count_tokens(text):
    return len(encoding.encode(text))

# Set up OpenAI API
API_KEY = ''
if API_KEY == '': exit()
openai.api_key = API_KEY

MAX_TOKENS = 4096
RESPONSE_TOKENS = 256

conversation_history = ""
conversation_messages = [
    {"role": "system", "content": system_message}
]

def receive_messages():
    global conversation_history, conversation_messages

    while True:
        msg_received = client.recv(1024).decode()
        print(msg_received)

        # Update the conversation history
        conversation_messages.append({"role": "user", "content": msg_received})

        # Convert the conversation to string for token counting
        conversation_str = "\n".join([msg['content'] for msg in conversation_messages])
        
        # Check token count using tiktoken
        if count_tokens(conversation_str) > (MAX_TOKENS - RESPONSE_TOKENS):
            # Request a summary if conversation is too long
            summary_response = openai.Completion.create(
                engine="gpt-3.5-turbo",
                prompt=f"Summarize the following conversation:\n{conversation_str}",
                max_tokens=RESPONSE_TOKENS
            )
            summary = summary_response.choices[0].text.strip()
            conversation_messages = [{"role": "user", "content": summary}]

        # Get a response from OpenAI based on full conversation history
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_messages
        )
        response_msg = response.choices[0].message['content'].strip()
        conversation_messages.append({"role": "assistant", "content": response_msg})
        client.send(response_msg.encode())

        os.system('clear')
        print('\n'.join([msg['content'] for msg in conversation_messages]))
        

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9999))

client.send(ai_chat_name.encode()) # username

threading.Thread(target=receive_messages).start()
