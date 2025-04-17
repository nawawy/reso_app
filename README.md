# Reso Researcher Chat Agent

## Overview
This project implements a full-stack AI-powered search agent called **Reso Researcher Chat Agent**. It combines a Python-based backend with a React frontend to perform web searches, scrape articles, and extract structured data based on user-defined schemas. The backend leverages APIs like Serper for search and OpenAI for data extraction, while the frontend provides a user-friendly chat interface for interaction.

I tried fisrt open source llm models like mistral and llama but since I run on CPU it takes a lot of time to get the answers so I used gpt api instead to get use of server GPUs.

## Project Structure

- **backend/**: Contains the Python backend code.
  - `app/`: Main application folder.
    - `agent.py`: Core logic for scraping articles and extracting data using NLP and OpenAI.
    - `config.py`: Configuration file for API keys (loaded from `.env`).
    - `main.py`: FastAPI application to handle API requests.
    - `schemas.py`: Pydantic models for request validation.
    - `utils.py`: Utility functions for text processing and chunking.
  - `requirements.txt`: Lists Python dependencies.
  - `.env`: Stores environment variables like API keys (not included in version control).

- **frontend/**: Contains the React frontend code.
  - `src/`: Source folder for React components and styles.
    - `App.jsx`: Main React component for the chat interface.
    - `App.css`, `index.css`: Styling for the frontend.
  - `index.html`: Entry point for the React app.
  - `package.json`, `vite.config.js`: Configuration for the Vite build tool.
  - `.eslintrc.js`: ESLint configuration for linting.
  - `.gitignore`: Specifies files to ignore in version control.

## Features
- **Search Functionality**: Uses the Serper API to fetch search results based on user prompts.
- **Article Scraping**: Scrapes articles using the `newspaper3k` library.
- **Data Extraction**: Combines rule-based (spaCy) and AI-based (OpenAI) methods to extract fields like title, authors, and dates.
- **Frontend Interface**: A React-based chat UI built with Material-UI for user interaction.
- **Backend API**: FastAPI server to handle search requests and return extracted data.

## Prerequisites
- **Python 3.8+**: For the backend.
- **Node.js 18+**: For the frontend.
- API keys for:
  - [Serper API](https://serper.dev/) (for search).
  - [OpenAI API](https://openai.com/) (for data extraction).

## Architecture Overview

### Backend (FastAPI)

- **Framework**: FastAPI for building a high-performance API.
- **Components**:
  - `main.py`: Defines the FastAPI app and API endpoints.
  - `agent.py`: Handles search, web scraping, and data extraction using Serper API, OpenAI, and spaCy.
  - `schemas.py`: Pydantic models for request validation.
  - `utils.py`: Utility functions for text processing.
  - `config.py`: Loads environment variables for API keys.
- **Flow**:
  1. Receives a search query and schema from the frontend.
  2. Fetches search results using the Serper API.
  3. Scrapes articles and extracts data using NLP (spaCy) and OpenAI.
  4. Returns results in both text and CSV format.

### Frontend (React)

- **Framework**: React with Vite for a fast development experience.
- **Components**:
  - `App.jsx`: Main component handling the chat interface, state management, and API calls.
  - Styling with Material-UI and custom CSS (`App.css`, `index.css`).
- **Flow**:
  1. User inputs a search prompt and optional schema.
  2. Sends a POST request to the backend `/search` endpoint.
  3. Displays results in a chat-like interface with Material-UI components.

## API Documentation

### Endpoint: `/search`

- **Method**: `POST`
- **Description**: Processes a search query and returns extracted data based on the provided schema.
- **Request Body**:

  ```json
  {
    "prompt": "string",  // Search query (required)
    "schema": "string"   // JSON string of fields to extract, e.g., `["title", "authors"]` (required)
  }
  ```
- **Response**:
  - **Success (200)**:

    ```json
    {
      "text_result": "string",  // Formatted text of extracted data
      "csv_content": "string"   // CSV-formatted data
    }
    ```
  - **Error (400/500)**:

    ```json
    {
      "error": "string",
      "text_result": "",
      "csv_content": ""
    }
    ```
- **CORS**: Enabled for all origins (adjust `allow_origins` in `main.py` for production).

## Setup Instructions

### Backend
1. Navigate to the `backend/` directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install the spaCy model:
   ```bash
   python -m spacy download en_core_web_sm
   ```
5. Set up environment variables in a `.env` file:
   ```plaintext
   SERPER_API_KEY=your_serper_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```
6. Run the FastAPI server:
   ```bash
   cd app
   uvicorn main:app --reload

   If faced errors this might help :
   python -m uvicorn main:app --reload
   
   ```

### Frontend
1. Navigate to the `frontend/` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   npm install @mui/material @emotion/react @emotion/styled
   npm install tailwindcss @tailwindcss/vite
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173` (or the port specified by Vite).

## Usage
1. Open the frontend in your browser.
2. Enter a search prompt (e.g., "Elon Musk biography") and an optional schema in JSON format (e.g., `["title", "authors", "summary"]`).
3. Click "Send" to initiate the search.
4. The backend will fetch search results, scrape articles, extract data, and display the results in the chat interface.

## Example
- **Prompt**: "Elon Musk biography"
- **Schema**: `["title", "authors", "summary"]`
- **Output**: The chat will display extracted data from the top search result, such as the article title, authors, and any identified dates of birth.

## Dependencies
### Backend
- `fastapi`: For the API server.
- `httpx`: For asynchronous HTTP requests.
- `spacy`: For NLP-based data extraction.
- `openai`: For AI-based data extraction.
- `newspaper3k`: For article scraping.
- `nltk`, `langchain`: For text processing.

### Frontend
- `react`: For the UI.
- `@mui/material`: For Material-UI components.
- `vite`: For the build tool.

## Notes
- Ensure your API keys are kept secure and not exposed in version control.
- The backend API runs on `http://localhost:8000` by default. Update the frontend fetch URL in `App.jsx` if you change the backend port or host.
- The schema field in the frontend is optional but must be valid JSON if provided.

## Troubleshooting
- **Backend Errors**:
  - If the Serper or OpenAI API fails, check your API keys in the `.env` file.
  - Ensure the spaCy model (`en_core_web_sm`) is installed.
- **Frontend Errors**:
  - If the frontend cannot connect to the backend, verify that the backend server is running and the fetch URL in `App.jsx` is correct.
  - Check the browser console for CORS-related errors and adjust the CORS settings in `main.py` if needed.

  ## Future Improvement Suggestions

- **Enhanced Error Handling**: Add more detailed error messages and logging for both backend and frontend to improve debugging and user feedback.
- **Schema Validation**: Implement stricter schema validation on the frontend and backend to ensure users provide valid JSON arrays for the schema field.
- **Caching Mechanism**: Introduce caching (e.g., Redis) for search results to reduce API calls and improve response times for repeated queries.
- **Advanced NLP Features**: Expand the NLP capabilities by integrating more advanced models for entity extraction or supporting additional fields like sentiment analysis.
- **User Authentication**: Add user authentication and session management to allow personalized search histories and settings.
- **Improved UI/UX**: Enhance the frontend with features like downloadable CSV files, better formatting of results, and a more interactive chat interface (e.g., support for follow-up questions).
- **Rate Limiting**: Implement rate limiting on the backend to prevent abuse of the API and ensure fair usage of external API keys.
- **Testing**: Add unit and integration tests for both backend and frontend to ensure reliability and maintainability as the project grows.