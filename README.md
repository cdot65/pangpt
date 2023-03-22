# FastAPI-PAN-OS-ChatGPT

This project is an implementation of a FastAPI application that receives firewall log messages from a Palo Alto Networks PAN-OS device, parses the messages, and sends the interesting information to OpenAI's GPT-3.5-turbo chatbot for troubleshooting. The chatbot's response is posted in a Slack channel. The project uses FastAPI for handling the HTTP requests, Slack API for posting messages to the Slack channel, and OpenAI API for interacting with the GPT-3.5-turbo chatbot.

## Project Setup

### Prerequisites

There are two methods to deploying, either locally with Poetry or through a Docker container. These docs will cover the Docker based installation:

- Python 3.6 or higher
- Python Poetry
- Slack application tokens
- OpenAI API token
- Docker

### Installation

1. Clone the repository from GitHub.
2. Create a virtual environment using the command `poetry install`.
3. Activate the virtual environment using the command `poetry shell`.
4. Set the following environment variables:

- SLACK_APP_TOKEN: Slack App token
- SLACK_BOT_TOKEN: Slack Bot token
- SLACK_CHANNEL: Slack channel to post the message
- OPENAI_TOKEN: OpenAI API key

### Running the Application

Build the Docker image using the command `invoke build`; macOS users on Apple silicon can use the command `invoke build --arm`.

Run the Docker container using the command `invoke local` (or `invoke local --arm` for Apple silicon).

### Usage

Once the FastAPI application is up and running, you can send a firewall log message to the `/pangpt/decryption/` endpoint using a POST request. The request should contain the firewall log message in JSON format.

```http
POST /pangpt/decryption/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
    "message": "Firewall decryption log message"
}
```

The FastAPI application will parse the message and send the interesting information to OpenAI's GPT-3.5-turbo chatbot for troubleshooting. The chatbot's response will be posted in the Slack channel specified in the SLACK_CHANNEL environment variable.

### API Documentation

The FastAPI application uses the OpenAPI specification to document the API. The API documentation is available at the /docs endpoint when the application is running. You can also access the OpenAPI schema at the /openapi.json endpoint.

### Project Structure

The project structure is as follows:

```text
.
├── app
|    └── main.py
├── docker
|    ├── arm
|    |    ├── Dockerfile
|    |    └── requirements.txt
|    └── intel
|         ├── Dockerfile
|         └── requirements.txt
├── slack
|    └── manifest.yaml
├── pyproject.toml
├── README.md
└── tasks.py

- `app`: The directory containing the FastAPI application files.
    - `main.py`: The main file containing the FastAPI application.
- `docker`: The directory containing the Docker files.
    - `arm`: The directory containing the Dockerfile and requirements.txt for ARM architecture.
        - `Dockerfile`: The Dockerfile for ARM architecture.
        - `requirements.txt`: The file containing the required Python packages for ARM architecture.
    - `intel`: The directory containing the Dockerfile and requirements.txt for Intel architecture.
        - `Dockerfile`: The Dockerfile for Intel architecture.
        - `requirements.txt`: The file containing the required Python packages for Intel architecture.
- `slack`: The directory containing the Slack files.
    - `manifest.yaml`: The manifest file for the Slack app.
- `pyproject.toml`: The file containing the project dependencies.
- `README.md`: The project documentation file.
- `tasks.py`: The Invoke tasks file.
```
