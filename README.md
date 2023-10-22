# TCP AI Chat Room
(c) 2021-2023 Kerry Fraser-Robinson

## Description:
TCP AI Chat Room is a simple Python-based chatroom where users can interact with each other and an AI chatbot. The project consists of a server (`server.py`), a regular chat client (`client.py`), and an AI-powered chat client (`ai_client.py`).

## Dependencies:
- Python 3.x (inc. `socket`, `threading`)
- `openai` (required for `ai_client.py`)
- `tiktoken` (required for `ai_client.py`)

## Usage:

### Server (`server.py`):
- Start the server by executing `server.py`.
- The server supports a special `/shutdown` command which can be used by an admin named "SysOp" to shut down the server remotely.

### Client (`client.py`):
- Start the client by executing `client.py`.
- Enter the server IP and port when prompted.
- The client will receive and display messages from the server.

### AI Client (`ai_client.py`):
- Start the AI client by executing `ai_client.py`.
- The AI client, named "ai_George", specializes in comedy and aims to entertain users.
- The AI client has a set of guidelines it follows for interactions. For instance, it can respond with `<listens>` if it doesn't have any new information to contribute to the conversation.

## Development:
Developers can extend the functionality by adding more features to the server and clients. For instance, the AI client's behavior and attributes can be adjusted by changing the parameters in `ai_client.py`.
