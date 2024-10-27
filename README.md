# AI Planet Internship Assignment

This is a FastAPI application. It uses the `uvicorn` server to run the application.

## API endpoints
1. /upload : This endpoint accepts a file and stores it in the local file system.
2. /ask : This end point accepts a string (question) and returns a response from the AI model.
Both endpoints render the same homepage.html template

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/itsvineetkr/ai-planet.git
    cd ai-planet
    ```

2. **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Setting up the .env file

1. **Create a `.env` file in the root directory of your project.**

2. **Add the following environment variables to the `.env` file:**
    ```env
    HUGGINGFACEHUB_API_TOKEN = "hf_----xxxxxxx----"
    ```
    Replace `hf_----xxxxxxx----` and `<your-secret-key>` with your huggingface api key.

## Running the Application

1. **Start the FastAPI server:**
    ```bash
    python main.py
    ```

    The application will be available at `http://localhost:8000/`.
